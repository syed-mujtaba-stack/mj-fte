import os
import click
from pathlib import Path
from typing import Optional, List

from mj.auth.google_oauth import GoogleOAuth
from mj.analyzer.scanner import FileScanner
from mj.analyzer.classifier import FileClassifier, FileCategory
from mj.analyzer.storage import StorageAnalyzer
from mj.cleaner.safe_delete import SafeCleaner, CleanAction
from mj.config.settings import settings
from mj.cli.ui import console, print_banner, print_section


def check_auth() -> bool:
    if os.getenv("MJ_SKIP_AUTH") == "1":
        return True
    oauth = GoogleOAuth()
    if not oauth.is_authenticated():
        console.print("[red]Not authenticated. Run [bold]mj init[/] first.[/]")
        return False
    return True


@click.group(invoke_without_command=True)
@click.version_option(version=settings.app_version, prog_name=settings.app_name)
@click.pass_context
def cli(ctx):
    """MJ FTE - System Analyst & Cleaner for Windows"""
    if ctx.invoked_subcommand is None:
        print_banner()
        console.print("Run [bold]mj --help[/] for available commands.\n")


@cli.command()
@click.option("--force", "-f", is_flag=True, help="Force re-authentication")
def init(force: bool):
    """Initialize MJ FTE with Google authentication"""
    print_banner()
    print_section("Initialization")

    oauth = GoogleOAuth()

    if oauth.is_authenticated() and not force:
        user = oauth.load_user()
        if user:
            console.print(f"[OK] Already authenticated as [bold]{user.email}[/]")
            console.print("Use [bold]mj init --force[/] to re-authenticate.")
            return

    if not settings.google_client_id or not settings.google_client_secret:
        console.print("[red][X] Google OAuth credentials not configured![/]")
        console.print("\nPlease set these environment variables or create a .env file:")
        console.print("  GOOGLE_CLIENT_ID=your_client_id")
        console.print("  GOOGLE_CLIENT_SECRET=your_client_secret")
        console.print("\nGet credentials from: https://console.cloud.google.com/apis/credentials")
        return

    success = oauth.authenticate()
    if success:
        console.print("\n>> [bold green]MJ FTE initialized successfully![/]")
        console.print("Run [bold]mj analyze[/] to scan your system.")
    else:
        console.print("\n[X] [bold red]Initialization failed.[/]")


@cli.command()
@click.option("--drive", "-d", default="C:\\", help="Drive to analyze")
@click.option("--depth", type=int, default=10, help="Max scan depth")
@click.option("--workers", "-w", type=int, default=4, help="Parallel workers")
@click.option("--min-size", type=float, default=1.0, help="Minimum file size in MB")
@click.option("--no-progress", is_flag=True, help="Disable progress bar")
def analyze(drive: str, depth: int, workers: int, min_size: float, no_progress: bool):
    """Analyze system for junk, dangerous files, and storage usage"""
    print_banner()

    if not check_auth():
        return

    print_section("System Analysis")

    scanner = FileScanner(
        root=drive,
        max_depth=depth,
        workers=workers,
    )

    console.print(f"Scanning [bold]{drive}[/] (depth: {depth}, workers: {workers})...\n")

    if no_progress:
        result = scanner.scan()
    else:
        result = scanner.scan_with_progress()

    console.print(f"\n[OK] Scan complete in {result.scan_duration:.1f}s")
    console.print(f"Total files: [bold]{result.total_files:,}[/]")
    console.print(f"Total size: [bold]{_format_size(result.total_size)}[/]")

    classifier = FileClassifier()
    classifications = classifier.classify_batch(result.files)

    for c in classifications:
        if c.category == FileCategory.JUNK:
            c.file.is_junk = True
        elif c.category == FileCategory.DANGEROUS:
            c.file.is_dangerous = True
    result.rebuild()

    junk = [c for c in classifications if c.category == FileCategory.JUNK]
    dangerous = [c for c in classifications if c.category == FileCategory.DANGEROUS]
    protected = [c for c in classifications if c.category == FileCategory.PROTECTED]
    normal = [c for c in classifications if c.category == FileCategory.NORMAL]

    console.print(f"\n>> Classification Results:")
    console.print(f"  [red]Junk:[/] {len(junk)} files ({_format_size(sum(c.file.size for c in junk))})")
    console.print(f"  [red]Dangerous:[/] {len(dangerous)} files ({_format_size(sum(c.file.size for c in dangerous))})")
    console.print(f"  [green]Protected:[/] {len(protected)} files ({_format_size(sum(c.file.size for c in protected))})")
    console.print(f"  [white]Normal:[/] {len(normal)} files ({_format_size(sum(c.file.size for c in normal))})")

    if junk:
        console.print_file_list("Junk Files", junk)

    if dangerous:
        console.print_file_list("Dangerous Files", dangerous)

    storage = StorageAnalyzer(drive).analyze(result, scan_root=drive)
    console.print_storage_info(storage)

    result._classifications = classifications
    ctx = click.get_current_context()
    ctx.obj = {"result": result, "classifications": classifications, "storage": storage}


@cli.command()
@click.option("--drive", "-d", default="C:\\", help="Drive to clean")
@click.option("--junk", is_flag=True, default=True, help="Clean junk files")
@click.option("--dangerous", is_flag=True, default=False, help="Clean dangerous files")
@click.option("--no-confirm", is_flag=True, help="Skip per-file confirmation")
@click.option("--dry-run/--no-dry-run", default=True, help="Dry run (default: true)")
@click.option("--batch", is_flag=True, help="Batch confirm (confirm once for all)")
def clean(drive: str, junk: bool, dangerous: bool, no_confirm: bool, dry_run: bool, batch: bool):
    """Clean junk and/or dangerous files with confirmation"""
    print_banner()

    if not check_auth():
        return

    print_section("Clean Operation")

    if not junk and not dangerous:
        console.print("[yellow]Nothing to clean. Use --junk and/or --dangerous[/]")
        return

    categories = []
    if junk:
        categories.append(FileCategory.JUNK)
    if dangerous:
        categories.append(FileCategory.DANGEROUS)

    scanner = FileScanner(root=drive)
    console.print(f"Scanning [bold]{drive}[/]...")
    result = scanner.scan_with_progress()

    classifier = FileClassifier()
    classifications = classifier.classify_batch(result.files)

    actionable = [c for c in classifications if c.category in categories and c.is_actionable]

    if not actionable:
        console.print("[green][OK] No actionable files found.[/]")
        return

    console.print(f"\nFound [bold]{len(actionable)}[/] actionable files:")
    junk_files = [c for c in actionable if c.category == FileCategory.JUNK]
    danger_files = [c for c in actionable if c.category == FileCategory.DANGEROUS]
    if junk_files:
        console.print(f"  [red]Junk:[/] {len(junk_files)} files ({_format_size(sum(c.file.size for c in junk_files))})")
    if danger_files:
        console.print(f"  [red]Dangerous:[/] {len(danger_files)} files ({_format_size(sum(c.file.size for c in danger_files))})")

    if dry_run:
        console.print("\n[yellow][!]  DRY RUN MODE - No files will be deleted[/]")
        if not console.confirm("Proceed with dry run?"):
            return
    else:
        console.print("\n[red][!]  LIVE MODE - Files will be moved to Recycle Bin[/]")
        if not console.confirm("Are you sure you want to proceed?"):
            return

    cleaner = SafeCleaner(
        dry_run=dry_run,
        confirm_each=not (no_confirm or batch),
    )

    def batch_confirm(classification):
        return CleanAction.DELETE

    def per_file_confirm(classification):
        size_str = _format_size(classification.file.size)
        reasons = ", ".join(classification.reasons)
        if console.confirm(f"Delete [bold]{classification.file.path.name}[/] ({size_str})?\n  Reason: {reasons}"):
            return CleanAction.DELETE
        return CleanAction.SKIP

    confirm_cb = batch_confirm if batch else per_file_confirm

    with console.progress_bar("Cleaning") as progress:
        task = progress.add_task("Cleaning...", total=len(actionable))

        def progress_cb(current, total, path):
            progress.update(task, completed=current, description=f"Cleaning: {path.name}")

        cleaner.progress_callback = progress_cb
        results = cleaner.clean(classifications, categories, confirm_cb)

    summary = cleaner.get_summary(results)
    console.print_clean_summary(summary)

    if dry_run:
        console.print("\n[blue]This was a dry run. Run with [bold]--no-dry-run[/] to actually clean.[/]")


@cli.command()
def status():
    """Show authentication and configuration status"""
    print_banner()
    print_section("Status")

    oauth = GoogleOAuth()

    console.print_kv("Authenticated", "Yes" if oauth.is_authenticated() else "No")
    if oauth.is_authenticated():
        user = oauth.load_user()
        if user:
            console.print_kv("User", user.email)
            console.print_kv("Name", user.name)

    console.print_kv("Config Dir", str(settings.config_dir))
    console.print_kv("Data Dir", str(settings.data_dir))
    console.print_kv("Scan Root", settings.scan_root)
    console.print_kv("OpenRouter Model", settings.openrouter_model)


@cli.command()
def logout():
    """Logout and clear stored credentials"""
    print_banner()
    print_section("Logout")

    oauth = GoogleOAuth()
    if oauth.is_authenticated():
        if console.confirm("Logout and remove stored credentials?"):
            oauth.logout()
    else:
        console.print("Not currently authenticated.")


@cli.command()
@click.option("--port", "-p", default=8080, help="Port for OAuth callback")
def auth_test(port: int):
    """Test OAuth configuration"""
    print_banner()
    print_section("OAuth Test")

    if not settings.google_client_id or not settings.google_client_secret:
        console.print("[red][X] Credentials not set[/]")
        return

    oauth = GoogleOAuth()
    auth_url = oauth.get_auth_url()
    console.print(f"Auth URL: {auth_url}")
    console.print("OAuth configuration appears valid.")


def _format_size(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


if __name__ == "__main__":
    cli()
