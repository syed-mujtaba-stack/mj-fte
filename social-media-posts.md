# MJ FTE — Social Media Launch Kit

> Sab posts English mein hain (international audience). Copy-paste karo aur apni timing pe post karo.
> Best posting time (PKT): Reddit/X = raat 6–10 PM, LinkedIn/Facebook = subah 9–11 AM

---

## 🟠 REDDIT — r/Python (sabse important!)

**Title:**
```
I built MJ FTE — an open-source Windows disk cleaner CLI that classifies every file before touching it
```

**Body:**
```
Like most of you, my C: drive was constantly full and I never knew exactly what was safe to delete. Built-in Disk Cleanup is opaque, and random "cleaner" apps from the internet feel risky.

So over the past few weeks I built **MJ FTE**, a Python CLI agent that:

- Scans your drives in parallel and classifies every file as junk / dangerous / protected — with a reason shown for each one
- Never touches Windows system paths (C:\Windows, Program Files, ProgramData are hard-blocked) — verified: a full C:\Windows scan returns ZERO actionable files
- Checks file attributes too (SYSTEM/HIDDEN/READONLY files are skipped)
- Cleans only after per-file approval, and moves everything to the Recycle Bin so it's fully recoverable
- Dry-run mode is the default — you see exactly what would happen before anything happens
- Uses Google OAuth sign-in (browser flow, tokens stored locally)

Tech stack: Python 3.12, Rich (TUI), Click, pywin32, send2trash, google-auth-oauthlib.

Install:
    pip install mj-fte
Then just run: mj init → mj analyze → mj clean --junk

GitHub: https://github.com/syed-mujtaba-stack/mj-fte
Website & docs: https://mjfte.vercel.app
PyPI: https://pypi.org/project/mj-fte/

It's MIT licensed and I'd genuinely love feedback — especially on the classification rules. What junk patterns do you wish it detected? What would make you trust a cleaner tool more?
```

> ⚠️ Note: r/windows aur r/opensource pe bhi same week mein post karo (title thoda change kar dena har jagah). Har subreddit ke rules pehle parh lo.

---

## 🐦 X / TWITTER — Thread

**Tweet 1 (Hook):**
```
Your Windows PC has thousands of junk files right now.

I built an open-source CLI that finds them, shows you exactly why each one is flagged, and cleans only what YOU approve.

Here's MJ FTE 🧵👇
```

**Tweet 2:**
```
mj analyze scans your entire drive in parallel:

🟡 Junk: 342 files (2.8 GB)
🔴 Dangerous: 12 executables
🟢 Protected: 41,203 Windows files (untouchable)
⚪ Normal: everything else

With a reason for every single flag.
```

**Tweet 3:**
```
Safety isn't a feature, it's the foundation:

• C:\Windows & Program Files hard-blocked
• SYSTEM/HIDDEN/READONLY attributes respected
• Dry-run by default
• Every deletion goes to Recycle Bin
• You approve each file
```

**Tweet 4:**
```
Zero setup. One Google sign-in via browser and you're in.

pip install mj-fte
mj init
mj analyze

MIT licensed, open source ⬇️
github.com/syed-mujtaba-stack/mj-fte
```

---

## 💼 LINKEDIN

```
🚀 Excited to share my latest open-source project: MJ FTE

Every Windows user knows the frustration — storage full, no idea what's safe to delete. Existing cleaners are either opaque black boxes or sketchy adware.

So I built something different: a CLI agent that treats transparency as a core feature.

What makes it unique:

▸ Every file gets classified (junk / dangerous / protected) WITH a visible reason
▸ Windows system directories are hard-blocked at the code level — not by "being careful"
▸ Nothing deletes without explicit approval, and everything goes to the Recycle Bin
▸ Dry-run mode is the default behavior

Built with Python, FastAPI ecosystem tools, Google OAuth, and a terminal UI powered by Rich.

📦 pip install mj-fte
🔗 https://github.com/syed-mujtaba-stack/mj-fte
🌐 https://mjfte.vercel.app

Building this taught me a lot about Windows filesystem internals, OAuth flows, and designing APIs where "safe" is the default state — not an option.

Would love feedback from fellow developers, especially on the classification heuristics. What would you add?

#opensource #python #windows #cli #softwareengineering #buildinpublic
```

---

## 📸 INSTAGRAM

**Format:** Carousel ya single screenshot (terminal ka dark theme screenshot best lagega)

**Caption:**
```
POV: Your C: drive is red but you're scared to delete anything 😤

Meet MJ FTE — a free open-source CLI that:
🔍 Finds all junk files on your PC
🛡️ NEVER touches Windows system files
✅ Asks YOUR permission before deleting anything
🗑️ Moves to Recycle Bin (100% recoverable)

One command install 👇
pip install mj-fte

Link in bio 🔗 | Star it on GitHub if you like it!

#windows11 #pctips #tech #coding #opensource #python #developer #diskcleanup #pchoes #software #programming #techtok #windows10 #pcbuilding
```

---

## 📘 FACEBOOK

**(Personal profile ke liye):**
```
Windows users! 🖥️

Ever noticed your C: drive filling up but too scared to delete files because "what if it breaks Windows"? 😅

I've been building an open-source tool called MJ FTE that solves exactly this:

✅ Scans your whole PC and tells you exactly which files are junk
✅ Flags dangerous executables
✅ Shows how much storage you can free up
✅ Deletes ONLY what you approve — one file at a time
✅ Everything goes to Recycle Bin, so nothing is ever lost forever
✅ Windows system files are permanently off-limits

It's completely FREE and open source. Install is one command:
pip install mj-fte

Website: https://mjfte.vercel.app
Source code: https://github.com/syed-mujtaba-stack/mj-fte

Try it out and let me know what you think! Feedback chahiye sab se 🙏
```

**(Tech groups mein share karte waqt):** Same post + ye line shuru mein:
```
Made this in Python — sharing here for feedback from fellow devs!
```

---

## 🎥 VIDEO BANANA HAI? — HAAN, ZAROOR BANAO!

Video sabse zyada traffic lata hai (especially Instagram Reels + YouTube Shorts). Ye lo complete script:

### 📱 30–45 Second Reel/Short Script

| Time | Screen Pe | Voiceover/Text |
|------|-----------|----------------|
| 0–3 sec | Red C: drive bar dikhaao | **Hook:** "Your C: drive is FULL. Here's how to fix it safely." |
| 3–8 sec | Terminal type: `pip install mj-fte` | "One command install — it's open source." |
| 8–15 sec | `mj init` → browser popup → Google sign-in | "Sign in once with Google. That's it." |
| 15–28 sec | `mj analyze` → results table scroll | "It scans EVERYTHING and shows you exactly what's junk — with reasons." |
| 28–38 sec | `mj clean --junk --no-dry-run` → y/n prompts dikhao | "Deletes ONLY what you approve. Everything goes to Recycle Bin." |
| 38–45 sec | Storage before/after ya final summary | "Free, open source. Link in bio. Star it on GitHub!" |

### Recording Tips:
1. **OBS Studio** (free) se record karo — 1080p minimum
2. Terminal ko **fullscreen dark theme** pe rakho (Rich TUI already beautiful hai)
3. Typing real karo, speed-up editing mein karna (CapCut free hai)
4. Background music: YouTube Audio Library se copyright-free lo
5. **Vertical (9:16)** record karo Reels/Shorts ke liye
6. Ek hi video 3 jagah daldo: YouTube Shorts + Instagram Reel + TikTok

### Video Post Caption:
```
This free CLI cleaned 2.8GB of junk from my PC — without touching a single Windows file 😳

pip install mj-fte
Full source code on GitHub (link in bio)

#windows #pctips #tech #coding #opensource
```

---

## 📅 Posting Schedule (suggested)

| Day | Action |
|-----|--------|
| Day 1 | Reddit r/Python + personal Facebook |
| Day 2 | X thread + LinkedIn |
| Day 3 | Instagram + tech FB groups |
| Day 4–5 | r/windows, r/opensource, Show HN |
| Weekend | Video record + Reels/Shorts upload |

⚠️ **Golden rule:** Ek hi din sab jagah spam mat karo — algorithm aur mods dono naraz hote hain. 1 platform/day.
