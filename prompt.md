# MJ FTE Website — Master Prompt for Lovable

> Copy everything below the line and paste it into Lovable (lovable.dev).
> Lovable stack: Vite + React + TypeScript + Tailwind + shadcn/ui.

---

Build a stunning, production-quality marketing + documentation website for **MJ FTE** — an open-source Windows disk cleaner & system analyzer CLI agent written in Python.

## Official Links (use these EXACT URLs everywhere)

- **GitHub Repo:** https://github.com/syed-mujtaba-stack/mj-fte
- **PyPI Package:** https://pypi.org/project/mj-fte/
- **Issues:** https://github.com/syed-mujtaba-stack/mj-fte/issues
- **Changelog:** https://github.com/syed-mujtaba-stack/mj-fte/blob/main/CHANGELOG.md
- **Install command:** `pip install mj-fte`

## Tech Stack

Vite + React + TypeScript + Tailwind CSS + shadcn/ui components, Lucide icons, Framer Motion animations. Fully responsive, dark theme only.

## Brand & Design Direction

- Product name: **MJ FTE** — tagline: *"Tera system, meri zimmedari"* (Your system, my responsibility)
- Premium dark aesthetic: background `#070B14`, cards `#0D1424` with subtle borders (`#1E293B`)
- Accent gradient: cyan (`#22D3EE`) → violet (`#A78BFA`), used sparingly on headings, buttons, glows
- Fonts: Space Grotesk (headings), Inter (body), JetBrains Mono (all code/terminal text)
- Glassmorphism sticky navbar with blur backdrop
- Framer Motion: fade-up reveals on scroll, hover lift on cards, animated gradient glow behind hero
- Subtle grid/noise background texture, radial glow orbs

## Pages / Sections

Single-page landing (`/`) + separate Docs page (`/docs`).

### 1. Navbar (sticky, glass)

Logo "MJ FTE" (terminal icon) | links: Features, How it Works, Safety, Commands, Versions, Docs | GitHub button → https://github.com/syed-mujtaba-stack/mj-fte | PyPI button → https://pypi.org/project/mj-fte/

### 2. Hero

- Badge pills: `PyPI v0.1.3` • `Python 3.12+` • `Windows 10/11` • `MIT License`
- Live shields.io badges:
  - `https://img.shields.io/github/stars/syed-mujtaba-stack/mj-fte?style=social`
  - `https://img.shields.io/pypi/v/mj-fte`
  - `https://img.shields.io/pypi/dm/mj-fte`
- H1: "Your Windows PC, Analyzed & Cleaned by AI-grade Rules"
- Subtext: "MJ FTE scans your drives for junk files and dangerous executables, shows full storage breakdown, and safely cleans them — with your approval on every file. Secured with Google OAuth. Never touches Windows system files."
- Primary CTA button: `pip install mj-fte` (with copy-to-clipboard icon)
- Secondary CTA: "⭐ Star on GitHub" → https://github.com/syed-mujtaba-stack/mj-fte
- Below hero: animated terminal mockup window (mac-style dots) showing this session:

```
$ mj init
[OK] Already authenticated as user@gmail.com

$ mj analyze
Scanning C:\ ... ████████████ 100%
[OK] Scan complete in 42.3s · 128,493 files

>> Classification Results:
  Junk:       342 files   (2.8 GB)
  Dangerous:   12 files   (156 MB)
  Protected: 41,203 files (18.4 GB)
  Normal:    86,936 files
```

Type out the terminal lines with a typing animation.

### 3. Features Grid (7 cards, icon + title + description)

1. 🔐 **Google OAuth Auth** — Secure "Continue with Google" login, zero passwords stored
2. 🔍 **Deep System Scan** — Parallel multi-threaded scanning with live progress tracking
3. 🗂️ **Smart Classification** — Junk, dangerous & protected categories with reasons for every file
4. 🛡️ **Windows Protection** — Hard-blocked system paths; verified: C:\Windows scan = 0 actionable files
5. 💾 **Storage Analysis** — Visual disk usage bar + top folders ranked by size
6. 🧹 **Safe Cleaning** — Dry-run default, per-file confirmation, Recycle Bin (fully recoverable)
7. 🎨 **Beautiful TUI** — Rich terminal UI with tables, progress bars and colors

### 4. How It Works (3-step horizontal timeline)

- **Step 1 — Authenticate:** run `mj init`, browser opens, sign in with Google. That's the only setup.
- **Step 2 — Analyze:** run `mj analyze`. Full drive scan classifies every file as junk / dangerous / protected.
- **Step 3 — Clean safely:** run `mj clean --junk`. Preview with dry-run, approve each file, everything goes to Recycle Bin.

### 5. Safety Section ("Why you can trust it")

Layered shield visual with 5 protection layers listed:

1. Hard blocklist: `C:\Windows`, `Program Files`, `ProgramData` never touched
2. User-profile protection: AppData (Microsoft, browsers, apps) excluded
3. Attribute checks: SYSTEM / HIDDEN / READONLY files skipped
4. Conservative rules: `.zip`, `.dll`, `.lnk` are NEVER flagged as junk
5. Recoverable by default: Recycle Bin + dry-run mode + per-file approval

### 6. Commands Reference (styled table, mono font)

| Command | What it does |
|---------|--------------|
| `mj init` | Google sign-in via browser (zero setup) |
| `mj analyze [--drive D:\] [--depth N] [--workers N] [--min-size MB]` | Full scan + storage report |
| `mj clean --junk [--dangerous]` | Clean junk/dangerous files |
| `mj clean --no-dry-run` | Actually delete (asks per file) |
| `mj clean --batch` | One confirmation for all files |
| `mj status` | Show auth + config status |
| `mj logout` | Remove stored credentials |

### 7. Configuration (.env table)

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | baked-in | Optional OAuth override |
| `OPENROUTER_API_KEY` | — | For AI features |
| `SCAN_ROOT` | `C:\` | Drive to scan |
| `MAX_SCAN_DEPTH` | `10` | Max folder depth |
| `PARALLEL_WORKERS` | `4` | Scan threads |
| `MIN_FILE_SIZE_MB` | `1.0` | Min file size to report |
| `USE_RECYCLE_BIN` | `true` | Recycle Bin instead of permanent delete |

Config file location: `%APPDATA%\MJ_FTE\.env`

### 8. Version History (vertical timeline, latest first) — use EXACTLY this content

**v0.1.3 — Latest**
Fixed crash on `mj init` after sign-in (duplicate legacy keyring methods overriding file storage). Added self-healing: missing user profile auto-recovered from saved token via `fetch_and_save_user()`.

**v0.1.2**
Zero-setup authentication: Google OAuth client baked into the package — users just sign in via browser. Token storage moved from Windows Credential Manager to `%APPDATA%\MJ_FTE\token.json` (fixes CredWrite 2560-byte blob limit error). Userinfo switched to lightweight requests call.

**v0.1.1**
One-time setup wizard in `mj init` with hidden secret input. Fixed credentials not loading outside project directory — settings now read `.env` from both CWD and `%APPDATA%\MJ_FTE\`.

**v0.1.0 — Initial Release**
Google OAuth flow, parallel filesystem scanner, junk/dangerous/protected classification engine, Windows protection rules, storage analysis, safe cleaner (dry-run default, per-file confirm, Recycle Bin), Rich TUI. Published to PyPI.

### 9. FAQ (accordion)

- **Is it safe?** Yes — dry-run default, Recycle Bin, per-file approval, hard system-path blocklist.
- **Does it need admin?** Not for user folders; admin gives deeper access.
- **Can I undo deletions?** Everything goes to Recycle Bin.
- **Which platforms?** Windows 10/11, Python 3.12+.

### 10. Footer

"Built with ❤ by syed-mujtaba-stack" | links: GitHub repo, PyPI package, MIT License, Changelog. Tagline again: "Tera system, meri zimmedari."

## Docs Page (`/docs` route)

Sidebar navigation (Getting Started, Installation, Authentication, Commands, Configuration, Safety, Version History). Render all the same content above in long-form documentation style with code blocks, tables and callout boxes (Tip/Warning).

Installation tabs:
```bash
# pip
pip install mj-fte

# uv
uv tool install mj-fte

# from source
git clone https://github.com/syed-mujtaba-stack/mj-fte.git
cd mj-fte
uv sync
```

## Quality Bar

Lighthouse-friendly: semantic HTML, alt texts, no layout shift. Every code snippet has a copy button. Smooth scroll to anchors. Make it look like a top-tier dev tool landing page (reference quality: linear.app / vercel.com polish).
