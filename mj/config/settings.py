import os
from pathlib import Path
from typing import List, Set
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


_appdata_dir = Path(os.getenv("APPDATA", str(Path.home()))) / "MJ_FTE"
_env_file_paths = (".env", str(_appdata_dir / ".env"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_env_file_paths,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "MJ FTE"
    app_version: str = "0.1.3"
    config_dir: Path = Field(
        default_factory=lambda: Path(os.getenv("APPDATA", Path.home())) / "MJ_FTE"
    )
    data_dir: Path = Field(
        default_factory=lambda: Path(os.getenv("LOCALAPPDATA", Path.home())) / "MJ_FTE"
    )

    # Google OAuth (baked-in defaults; override via env/.env)
    google_client_id: str = "319816556110-963l1cn7vqcvjtq069vki9puidh4hlmi.apps.googleusercontent.com"
    google_client_secret: str = "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"
    google_redirect_uri: str = "http://localhost:8080/callback"
    google_scopes: List[str] = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]

    # OpenRouter (for free models)
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "meta-llama/llama-3.1-8b-instruct:free"

    # Scanner
    scan_root: str = "C:\\"
    max_scan_depth: int = 10
    parallel_workers: int = 4
    min_file_size_mb: float = 1.0
    max_files_per_folder: int = 10000

    # Junk detection (conservative - only clearly disposable formats)
    junk_extensions: Set[str] = {
        ".tmp", ".temp", ".log", ".cache", ".bak", ".old", ".orig",
        ".dmp", ".crash", ".wer", ".etl", ".chk", ".gid", ".fts",
        ".pyc", ".pyo", ".class",
    }

    junk_folders: Set[str] = {
        "temp", "tmp", "cache", "caches", "logs", "log", "crashdumps",
        "minidump", "wer", "prefetch", "softwareDistribution", "download",
        "windows.old", "windows~bt", "$recycle.bin", "recycler",
        "thumbs.db", "desktop.ini", ".ds_store", ".spotlight-v100",
        ".trashes", ".fseventsd", "node_modules", "__pycache__",
        ".venv", "venv", "env", ".env", "dist", "build", "target",
        ".gradle", ".m2", ".ivy2", ".sbt", ".idea", ".vscode",
        ".vs", "bin", "obj", "packages", "out", "publish",
    }

    junk_file_patterns: List[str] = [
        "*.tmp", "*.temp", "*.log", "*.bak", "*.old", "*.orig",
        "*.dmp", "*.crash", "*.wer", "*.etl",
        "Thumbs.db", ".DS_Store",
        "*.chk", "*.gid", "*.fts",
        "*.pyc", "*.pyo",
    ]

    # Dangerous file detection (executable/script formats only)
    dangerous_extensions: Set[str] = {
        ".exe", ".bat", ".cmd", ".com", ".scr", ".pif", ".msi",
        ".msp", ".mst", ".ps1", ".ps1xml", ".ps2", ".ps2xml",
        ".psc1", ".psc2", ".psd1", ".psdm1", ".vbs", ".vbe",
        ".jse", ".ws", ".wsf", ".wsc", ".wsh", ".hta",
        ".appref-ms", ".application", ".gadget",
        ".msc", ".cpl", ".inf", ".reg", ".sct", ".shb", ".shs",
    }

    # Name-based suspicion - only checked when extension is already dangerous
    suspicious_names: Set[str] = {
        "crack", "keygen", "key-maker", "loader", "inject",
        "rootkit", "keylogger", "stealer", "miner", "ransom",
        "trojan", "malware", "spyware", "backdoor", "botnet",
    }

    # Windows protected paths (never touch)
    windows_protected_paths: List[str] = [
        "C:\\Windows",
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        "C:\\ProgramData",
        "C:\\Users\\Default",
        "C:\\Users\\Public",
        "C:\\System Volume Information",
        "C:\\Recovery",
        "C:\\$Recycle.Bin",
        "C:\\Boot",
        "C:\\EFI",
        "C:\\PerfLogs",
    ]

    # Protected folders under user profile (relative to %USERPROFILE%)
    user_protected_folders: Set[str] = {
        "appdata\\local\\microsoft",
        "appdata\\roaming\\microsoft",
        "appdata\\roaming\\microsoft\\windows",
        "appdata\\roaming\\microsoft\\windows\\start menu",
        "appdata\\roaming\\microsoft\\windows\\recent",
        "appdata\\roaming\\microsoft\\windows\\sendto",
        "appdata\\roaming\\microsoft\\windows\\templates",
        "appdata\\roaming\\microsoft\\windows\\start menu\\programs",
        "appdata\\roaming\\microsoft\\windows\\start menu\\programs\\startup",
        "appdata\\local\\packages",
        "appdata\\local\\microsoft\\windows",
        "appdata\\local\\microsoft\\windowsapps",
        "appdata\\local\\microsoft\\onedrive",
        "appdata\\local\\microsoft\\edge",
        "appdata\\local\\google\\chrome",
        "appdata\\local\\mozilla\\firefox",
        "appdata\\roaming\\mozilla\\firefox",
        "appdata\\roaming\\thunderbird",
        "appdata\\local\\microsoft\\outlook",
        "appdata\\roaming\\microsoft\\outlook",
        "appdata\\local\\microsoft\\teams",
        "appdata\\roaming\\microsoft\\teams",
        "appdata\\local\\slack",
        "appdata\\roaming\\slack",
        "appdata\\local\\discord",
        "appdata\\roaming\\discord",
        "appdata\\local\\zoom",
        "appdata\\roaming\\zoom",
        "appdata\\local\\notion",
        "appdata\\roaming\\notion",
        "appdata\\local\\obsidian",
        "appdata\\roaming\\obsidian",
        "appdata\\local\\vscode",
        "appdata\\roaming\\code",
        "appdata\\local\\jetbrains",
        "appdata\\roaming\\jetbrains",
    }

    # File attributes to protect (Windows)
    protected_attributes: Set[str] = {"SYSTEM", "HIDDEN", "READONLY"}

    # Cleaner
    use_recycle_bin: bool = True
    confirm_each_file: bool = True
    batch_confirm_threshold: int = 50
    dry_run_default: bool = True

    # UI
    console_width: int = 120
    show_progress: bool = True
    color_output: bool = True


settings = Settings()

# Ensure directories exist
settings.config_dir.mkdir(parents=True, exist_ok=True)
settings.data_dir.mkdir(parents=True, exist_ok=True)


def save_oauth_credentials(client_id: str, client_secret: str) -> Path:
    env_path = settings.config_dir / ".env"
    lines: List[str] = []
    if env_path.exists():
        content = env_path.read_text(encoding="utf-8")
        lines = [
            line for line in content.splitlines()
            if not line.strip().startswith(("GOOGLE_CLIENT_ID=", "GOOGLE_CLIENT_SECRET="))
        ]
    lines.insert(0, f"GOOGLE_CLIENT_SECRET={client_secret}")
    lines.insert(0, f"GOOGLE_CLIENT_ID={client_id}")
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return env_path