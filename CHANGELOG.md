# Changelog

All notable changes to **MJ FTE** are documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.3] — 2026-08-21

### Fixed
- **Crash on `mj init` after sign-in** — duplicate legacy `save_user` / `load_user` methods (still using the removed `keyring` import) were overriding the new file-based storage, raising `NameError: name 'keyring' is not defined`.
- Missing user profile is now **self-healed**: if a valid token exists but `user.json` is missing, MJ FTE fetches and saves the Google profile automatically via `fetch_and_save_user()`.

### Changed
- `fetch_and_save_user()` added as a reusable recovery method used by both `authenticate()` and `mj init`.

## [0.1.2] — 2026-08-21

### Added
- **Zero-setup authentication** — Google OAuth client credentials are now baked into the package. End users run `mj init`, the browser opens a Google tab, they sign in, done. No configuration of any kind.
- Direct browser flow: wizard is skipped entirely when built-in credentials are present.

### Changed
- **Token storage moved from Windows Credential Manager (keyring) to `%APPDATA%\MJ_FTE\token.json`.** Windows CredWrite has a ~2560-byte blob limit; OAuth token JSON (with JWT id_token) exceeded it, causing `(1783, 'CredWrite', 'The stub received bad data')`.
- `id_token` excluded from stored data (not needed at runtime).
- Userinfo endpoint switched from heavyweight `googleapiclient` discovery to a single lightweight `requests` call.

## [0.1.1] — 2026-08-21

### Added
- **One-time setup wizard** in `mj init`: prompts for Client ID / Secret when not configured, with hidden input for the secret. Saves to `%APPDATA%\MJ_FTE\.env`.

### Fixed
- **Credentials not found outside project directory** — settings now load `.env` from *both* the current working directory *and* `%APPDATA%\MJ_FTE\.env`, so the CLI works from any folder.

## [0.1.0] — 2026-08-20

Initial public release. Published to [PyPI](https://pypi.org/project/mj-fte/).

### Added
- 🔐 **Google OAuth authentication** — "Continue with Google" flow with local loopback callback server (`http://localhost:8080/callback`).
- 🔍 **Parallel filesystem scanner** — multi-threaded drive walker with live progress, configurable depth/workers/minimum file size.
- 🗂️ **Classification engine** — junk / dangerous / protected categories with reason reporting:
  - Junk: `.tmp`, `.log`, `.bak`, cache folders, build artifacts, etc.
  - Dangerous: executable/script extensions + suspicious name patterns (crack, keygen, rootkit…)
- 🛡️ **Windows protection rules** — hard blocklist (`C:\Windows`, `Program Files`, `ProgramData`…), user-profile protection (AppData Microsoft/browsers/apps), SYSTEM/HIDDEN/READONLY attribute checks. Verified: full `C:\Windows` scan yields **zero actionable files**.
- 💾 **Storage analysis** — disk usage bar, free space report, top folders by size.
- 🧹 **Safe cleaner** — dry-run by default, per-file or batch confirmation, Recycle Bin deletion via `send2trash`, graceful permission-error handling.
- 🎨 **Rich TUI** — ASCII banner, colored tables, progress bars, storage bar.
- CLI commands: `init`, `analyze`, `clean`, `status`, `logout`, `auth-test`.
