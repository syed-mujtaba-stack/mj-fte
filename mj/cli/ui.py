from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Confirm, Prompt
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from rich.markup import escape
from typing import Optional, List, Any
from pathlib import Path

from mj.config.settings import settings


class MJConsole:
    def __init__(self):
        self.console = Console(width=settings.console_width)

    def print(self, *args, **kwargs):
        self.console.print(*args, **kwargs)

    def print_banner(self):
        banner = Text()
        banner.append("  __  __ ____   __ _____ _____ \n", style="bold cyan")
        banner.append(" |  \\/  |  _ \\ /__|_   _|_   _|\n", style="bold cyan")
        banner.append(" | |\\/| | |_) | / _| | |   | |  \n", style="bold cyan")
        banner.append(" | |  | |  _ < | (_| | |   | |  \n", style="bold cyan")
        banner.append(" |_|  |_|_| \\_\\ \\__|_|_|   |_|  \n", style="bold cyan")
        banner.append("\n", style="")
        banner.append("  MJ FTE - System Analyst & Cleaner\n", style="bold yellow")
        banner.append('  "Tera system, meri zimmedari"\n', style="italic green")
        self.console.print(Panel(banner, border_style="bright_blue"))

    def print_section(self, title: str, style: str = "bold yellow"):
        self.console.print()
        self.console.print(f"[{style}]{'='*60}[/]")
        self.console.print(f"[{style}]  {title}[/]")
        self.console.print(f"[{style}]{'='*60}[/]")

    def print_kv(self, key: str, value: Any, key_style: str = "cyan", value_style: str = "white"):
        from rich.markup import escape
        self.console.print(f"[{key_style}]{escape(str(key))}:[/] [{value_style}]{escape(str(value))}[/]")

    def print_table(self, title: str, columns: List[str], rows: List[List[Any]], styles: List[str] = None):
        table = Table(title=title, show_header=True, header_style="bold magenta")
        for i, col in enumerate(columns):
            style = styles[i] if styles and i < len(styles) else None
            table.add_column(col, style=style)
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
        self.console.print(table)

    def print_file_list(self, title: str, files: List, max_show: int = 20):
        if not files:
            self.console.print(f"[green]No {title.lower()} found.[/]")
            return

        self.console.print(f"\n[bold]{title} ({len(files)} files)[/]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("File", style="white", ratio=3)
        table.add_column("Size", style="yellow", justify="right", width=12)
        table.add_column("Reason", style="red", ratio=2)

        for i, f in enumerate(files[:max_show]):
            size_str = self._format_size(f.size if hasattr(f, 'size') else f.file.size)
            reason = f.classification_reason if hasattr(f, 'classification_reason') else (f.reasons[0] if f.reasons else "")
            table.add_row(str(i+1), str(f.path.name if hasattr(f, 'path') else f.file.path.name), size_str, reason)

        if len(files) > max_show:
            table.add_row("...", f"and {len(files) - max_show} more", "", "")

        self.console.print(table)

    def print_storage_info(self, storage):
        self.print_section("Storage Analysis")

        bar_width = 50
        used_pct = storage.used_percentage
        filled = int(bar_width * used_pct / 100)
        bar = "#" * filled + "-" * (bar_width - filled)

        self.console.print(f"Drive: [bold]{escape(str(storage.drive))}[/]")
        self.console.print(f"[{'green' if used_pct < 70 else 'yellow' if used_pct < 90 else 'red'}]{bar}[/] {used_pct:.1f}% used")
        self.print_kv("Total", self._format_size(storage.total_space))
        self.print_kv("Used", self._format_size(storage.used_space))
        self.print_kv("Free", self._format_size(storage.free_space))
        self.print_kv("Junk", self._format_size(storage.junk_size), value_style="red")
        self.print_kv("Dangerous", self._format_size(storage.dangerous_size), value_style="red")
        self.print_kv("Protected", self._format_size(storage.protected_size), value_style="green")

        if storage.top_folders:
            self.console.print("\n[bold]Top Folders by Size:[/]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("#", style="dim", width=4)
            table.add_column("Folder", style="white", ratio=3)
            table.add_column("Size", style="yellow", justify="right", width=12)
            table.add_column("Files", style="cyan", justify="right", width=8)

            for i, folder in enumerate(storage.top_folders[:15]):
                table.add_row(str(i+1), str(folder.path), self._format_size(folder.size), str(folder.file_count))
            self.console.print(table)

    def print_clean_summary(self, summary: dict):
        self.print_section("Clean Summary")
        self.print_kv("Total Processed", summary.get('total', 0))
        self.print_kv("Deleted", summary.get('deleted', 0), value_style="green")
        self.print_kv("Skipped", summary.get('skipped', 0), value_style="yellow")
        self.print_kv("Failed", summary.get('failed', 0), value_style="red")
        self.print_kv("Space Freed", self._format_size(summary.get('space_freed', 0)), value_style="bold green")

        if summary.get('errors'):
            self.console.print("\n[red]Errors:[/]")
            for err in summary['errors'][:10]:
                self.console.print(f"  - {err}")

    def confirm(self, message: str, default: bool = True) -> bool:
        return Confirm.ask(f"[bold yellow]{message}[/]", default=default)

    def prompt(self, message: str, default: str = "", password: bool = False) -> str:
        return Prompt.ask(f"[bold cyan]{message}[/]", default=default, password=password)

    def _format_size(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} PB"

    def progress_bar(self, description: str = "Processing"):
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console,
        )


console = MJConsole()


def print_banner():
    console.print_banner()


def print_section(title: str, style: str = "bold yellow"):
    console.print_section(title, style)


def print_kv(key: str, value: Any, key_style: str = "cyan", value_style: str = "white"):
    console.print_kv(key, value, key_style, value_style)


def print_table(title: str, columns: List[str], rows: List[List[Any]], styles: List[str] = None):
    console.print_table(title, columns, rows, styles)