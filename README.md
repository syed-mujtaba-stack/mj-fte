# MJ FTE — CLI System Analyst & Cleaner for Windows

[![PyPI version](https://img.shields.io/pypi/v/mj-fte?color=blue&logo=pypi)](https://pypi.org/project/mj-fte/)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-0078D6?logo=windows95&logoColor=white)](https://pypi.org/project/mj-fte/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CLI](https://img.shields.io/badge/type-CLI%20Agent-orange)](https://pypi.org/project/mj-fte/)

> **"Tera system, meri zimmedari"** — Your system, my responsibility

**MJ FTE** is an open-source **Windows disk cleaner and system analyzer CLI agent** written in Python. It scans your drives to find **junk files, temporary files, and dangerous executables**, shows a full **disk storage breakdown**, and safely cleans them — with your approval on every file. Secured with **Google OAuth login** and protected by hard rules that never touch Windows system files.

## ✨ Features

- 🔐 **Google OAuth Authentication** - Secure "Continue with Google" login, no passwords stored
- 🔍 **Deep System Scan** - Parallel multi-threaded scanning with live progress tracking
- 🗂️ **Smart Classification** - Detects junk files, dangerous executables, and protected system files
- 🛡️ **Windows Protection** - Never touches `C:\Windows`, `Program Files`, or any system-critical path
- 💾 **Storage Analysis** - Visual disk usage bar + top folders by size
- 🧹 **Safe Cleaning** - Dry-run by default, per-file confirmation, Recycle Bin support (recoverable)
- 🎨 **Beautiful TUI** - Rich terminal interface with tables, progress bars, and colors

## 📦 Installation

Install from PyPI:

```bash
pip install mj-fte
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install mj-fte
```

### Prerequisites
- Python 3.12+
- Windows 10/11
- Google Cloud Console project with OAuth credentials (see setup below)

### Setup from source

1. **Clone and install:**
```bash
git clone https://github.com/syed-mujtaba-stack/mj-fte.git
cd mj-fte

# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

2. **Configure credentials:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Get Google OAuth credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Create OAuth 2.0 Client ID (Desktop app)
   - Add `http://localhost:8080/callback` as authorized redirect URI
   - Copy Client ID and Secret to `.env`

4. **Get OpenRouter API key (optional, for AI features):**
   - Sign up at [OpenRouter](https://openrouter.ai/keys)
   - Add key to `.env`

## Usage

### First Time Setup
```bash
mj init
```
Opens browser for Google authentication. Tokens stored securely in Windows Credential Manager.

### Analyze System
```bash
# Full C: drive scan (default)
mj analyze

# Custom options
mj analyze --drive D:\ --depth 5 --workers 8 --min-size 10
```

Shows:
- Junk files (temp, cache, logs, build artifacts, etc.)
- Dangerous files (executables, scripts in user folders)
- Protected Windows files (never touched)
- Storage breakdown with visual bar
- Top folders by size

### Clean Files
```bash
# Dry run (default) - shows what would be deleted
mj clean --junk

# Actually clean junk files
mj clean --junk --no-dry-run

# Clean dangerous files too (be careful!)
mj clean --junk --dangerous --no-dry-run

# Batch confirm (one prompt for all)
mj clean --junk --no-dry-run --batch

# Skip confirmations entirely
mj clean --junk --no-dry-run --no-confirm
```

### Other Commands
```bash
mj status      # Show auth and config status
mj logout      # Remove stored credentials
mj auth-test   # Test OAuth configuration
mj --help      # Show all options
```

## Configuration

All settings in `.env` or environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_CLIENT_ID` | - | OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | - | OAuth client secret |
| `OPENROUTER_API_KEY` | - | OpenRouter API key |
| `SCAN_ROOT` | `C:\` | Root drive to scan |
| `MAX_SCAN_DEPTH` | `10` | Max folder depth |
| `PARALLEL_WORKERS` | `4` | Scan threads |
| `MIN_FILE_SIZE_MB` | `1.0` | Min file size to report |

## Safety Features

### Protected Paths (Never Touched)
- `C:\Windows`, `C:\Program Files`, `C:\Program Files (x86)`
- `C:\ProgramData`, `C:\System Volume Information`
- User AppData folders for Microsoft, browsers, system apps
- Files with SYSTEM, HIDDEN, READONLY attributes

### Confirmation Modes
1. **Per-file** (default) - Confirm each file
2. **Batch** - One confirmation for all
3. **No-confirm** - Auto-delete (use with `--no-dry-run`)

### Dry Run Default
All clean operations default to dry-run. Use `--no-dry-run` to actually delete.

### Recycle Bin
Files are moved to Recycle Bin by default (recoverable). Controlled via `USE_RECYCLE_BIN=false` in `.env`.

### Dev Mode
Set `MJ_SKIP_AUTH=1` environment variable to bypass Google auth (development/testing only).

## File Classification

### Junk Extensions (conservative - clearly disposable only)
`.tmp`, `.temp`, `.log`, `.cache`, `.bak`, `.old`, `.orig`, `.dmp`, `.crash`, `.wer`, `.etl`, `.chk`, `.gid`, `.fts`, `.pyc`, `.pyo`, `.class`

### Junk Folders
`temp`, `tmp`, `cache`, `logs`, `crashdumps`, `prefetch`, `SoftwareDistribution\Download`, `Windows.old`, `$Recycle.Bin`, `node_modules`, `__pycache__`, `.venv`, `dist`, `build`, `target`, `.gradle`, `.idea`, `.vscode`, `.vs`, `bin`, `obj`, `packages`, `out`, `publish`

### Dangerous Extensions (executable/script formats)
`.exe`, `.bat`, `.cmd`, `.com`, `.scr`, `.pif`, `.msi`, `.ps1`, `.vbs`, `.vbe`, `.jse`, `.wsf`, `.wsh`, `.hta`, `.cpl`, `.inf`, `.reg`, `.msc`, `.gadget`

### Suspicious Names (only checked on dangerous extensions)
`crack`, `keygen`, `loader`, `inject`, `rootkit`, `keylogger`, `stealer`, `miner`, `ransom`, `trojan`, `malware`, `spyware`, `backdoor`, `botnet`

> **Note:** Archives (`.zip`, `.rar`, `.iso`), libraries (`.dll`), and shortcuts (`.lnk`) are NEVER flagged — too risky to assume they're junk.

## Architecture

```
mj/
├── __main__.py          # Entry point
├── cli/
│   ├── commands.py      # Click commands (init, analyze, clean, status)
│   └── ui.py            # Rich console UI
├── auth/
│   └── google_oauth.py  # Google OAuth flow + token storage
├── analyzer/
│   ├── windows_rules.py # Windows protection rules
│   ├── scanner.py       # Parallel filesystem scanner
│   ├── classifier.py    # File classification engine
│   └── storage.py       # Disk usage analysis
├── cleaner/
│   └── safe_delete.py   # Safe deletion with Recycle Bin
├── config/
│   └── settings.py      # Pydantic settings management
└── utils/
    └── (utilities)
```

## Troubleshooting

### "Not authenticated"
Run `mj init` first.

### "Permission denied" during scan
Run terminal as Administrator for full C: access.

### "Google OAuth failed"
- Check `.env` credentials
- Verify redirect URI in Google Console: `http://localhost:8080/callback`
- Ensure OAuth consent screen is configured

### Scan takes too long
- Reduce `--depth`
- Increase `--min-size`
- Exclude more folders in `settings.py`

## License

MIT License - Use at your own risk. Always backup important data.

## Disclaimer

**This tool deletes files.** While extensive protections exist, use at your own risk. Always:
1. Run `mj analyze` first
2. Review the file lists
3. Use `--dry-run` before `--no-dry-run`
4. Keep backups of important data

The authors are not responsible for any data loss.