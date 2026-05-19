# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### GCP Image Editing (Vertex AI Imagen Edit)
- **Script Location**: `/home/gateman/.openclaw/workspace/edit_image_skill.mjs`
- **Key File**: `/home/gateman/sa-key.json`
- **Proxy**: None (Running natively on GCP VM, no proxy required)
- **Project**: `jason-hsbc`
- **Usage**: `node edit_image_skill.mjs <image_path> <prompt> <output_path>`
- **Note**: The API (`imagen-3.0-generate-001:predict` in edit mode) may occasionally return 500 errors. If so, switch to pure text-to-image generation instead.

### Credentials
- **GitHub PAT**: `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` (User: nvd11, bound email: nvd11@163.com)
  - Also exported as `GITHUB_TOKEN` in `~/.bashrc` and `~/.profile`
- **ClawHub Token**: `clh_KIx-0ULhcKw9QyMLAYduTHrRNdQRVaJ7UtM9xhqJLoY` (User: @nvd11)
- **Gemini API Key**: `AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ`

### Sending Emails (Gmail SMTP)
- **Account**: `gateman56@gmail.com`
- **App Password**: `lekzjeuykwytooxj`
- **Method**: Use Python's built-in `smtplib` and `email` modules via `smtp.gmail.com` port `465` (SSL).
- **Example**: Create a `MIMEMultipart` message, attach `MIMEText`, `server.login(sender_email, password)`, and `server.sendmail(sender, receiver, msg.as_string())`.

### Daily Email Summary (Gmail IMAP)
- **Account**: `gateman56@gmail.com`
- **App Password**: `lekzjeuykwytooxj`
- **Location**: `~/workspace/skills/gmail-imap-summary/`
- **Files**: `fetch_emails.py` (recent 5), `daily_email_report.py` (all today)
- **Cron**: A background cron job (`daily-email-summary`) runs this at 09:00 AM daily.

### Gemini Image Remix (P图大师)
- **Tool**: `gemini-image-remix` (installed via ClawHub)
- **Script Location**: `/home/gateman/.openclaw/workspace/skills/gemini-image-remix/scripts/remix.py`
- **API Key Required**: Yes, `export GEMINI_API_KEY=AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ`
- **Env Required**: `export PATH="/home/gateman/.local/bin:$PATH"` (needs `uv` to run)
- **Usage Example (图生图/换背景/加元素)**:
  ```bash
  export GEMINI_API_KEY=AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ
  export PATH="/home/gateman/.local/bin:$PATH"
  uv run ~/workspace/skills/gemini-image-remix/scripts/remix.py --prompt "keep the people exactly the same, but add a large red cloth banner hanging across the VERY TOP..." -a "16:9" -i /path/to/input.png -f /path/to/output.png
  ```
- **Note**: When requesting banners with text, specify exact English text and give strict positional instructions (e.g., "VERY TOP near the ceiling, FAR ABOVE people's heads") so it doesn't cover faces. Chinese text is not reliably rendered by Gemini 2.5 Flash Image.
### Nano Banana API (DEPRECATED / MISLEADING)
- **Script Location**: `/home/gateman/.openclaw/workspace/nano_banana_skill.mjs`
- **Note**: WARNING - Discovered on 2026-05-13 that this script does NOT use Gemini 3 Pro Image. It is identical to `generate_image_skill.mjs` and uses Vertex AI's `imagen-3.0-generate-001`. It is NOT good at text rendering or structural diagrams. For real Gemini image capabilities, use the `gemini-image-remix` skill instead!

### Google Veo API (Video Generation)
- **Model**: `veo-3.1-generate-preview` (via Vertex AI)
- **Key File**: `/home/gateman/sa-key.json`
- **Project**: `jason-hsbc`
- **Location**: `us-central1`
- **Script**: `/home/gateman/.openclaw/workspace/veo_test.py`
- **Capabilities**: Can generate high-quality 4K short video clips (5-6 seconds) based on text or image prompts.
- **Core Implementation Requirements**:
  1. **Authentication**: Must use Service Account key via `os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/gateman/sa-key.json"`. Standard API Keys will fail with 403/401 for Vertex AI models.
  2. **SDK**: Must use the modern `google-genai` Python SDK (install via `uv pip install google-genai`). The old `@google-cloud/aiplatform` and REST APIs often return 404 on LRO polling.
  3. **LRO (Long-Running Operation)**: Video generation is not synchronous. You must call `client.models.generate_videos(...)`, obtain the `operation` object, and poll `client.operations.get(operation=op)` in a `while not op.done:` loop with a `time.sleep(10)`.
  4. **Parameters**: Ensure `person_generation="ALLOW_ADULT"` is set to avoid safety blocks on human generation. 

### Web Scraping & Paywall Bypass (CSDN)
- **Script Location**: `/home/gateman/.openclaw/workspace/scripts/fetch_csdn.py`
- **Usage**: `python3 ~/workspace/scripts/fetch_csdn.py <csdn_url>`
- **Core Principle**: Uses `Googlebot` User-Agent spoofing (`Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)`) to bypass CSDN/content-platform login walls designed for SEO, then extracts the `#content_views` div using `BeautifulSoup`.

### AWS Moon Proxy
- **Credentials**: Stored in `skills/aws-moon-proxy/SKILL.md`
- **Region**: `ap-southeast-1`
- **IP**: `13.212.67.185`

### Cloudflare
- **Email**: gateman56@gmail.com
- **API Token**: cfut_ZkmR1Ot6UHQ16JmAqOeDdaG7QnO5Hflew1ADSJ1s3f944b25

### Cloudflare
- **Email**: gateman56@gmail.com
- **API Token**: cfut_ZkmR1Ot6UHQ16JmAqOeDdaG7QnO5Hflew1ADSJ1s3f944b25

### Distributed GUI Browser Hijacking (Tailscale + Playwright)
- **Use Case**: Bypassing strict anti-bot systems (like LinkedIn's React synthetic event filters) that block JS DOM injections, while maintaining the user's logged-in session, without freezing the SSH tunnel with CDP backpressure.
- **Architecture**:
  - **Brain**: Runs on the headless server (GCP).
  - **Muscle**: Runs on the target GUI machine (Radxa Moon, IP `100.115.214.26` with XRDP+XFCE4) via SSH.
- **Setup on Target Machine (Radxa Moon)**:
  1. Restart Chrome with debugging port bound to localhost:
     `export DISPLAY=:10.0`
     `killall -9 chrome 2>/dev/null; sleep 1; rm -f ~/.config/google-chrome/SingletonLock; nohup /usr/bin/google-chrome-stable --remote-debugging-port=9222 --user-data-dir=/home/gateman/.config/google-chrome > /tmp/chrome_debug.log 2>&1 &`
  2. Setup isolated Playwright environment:
     `mkdir -p ~/projects/openclaw-stealth-agents && cd ~/projects/openclaw-stealth-agents`
     `python3 -m venv .venv`
     `.venv/bin/pip install playwright`
- **Execution**:
  - The script must use `sync_playwright` and connect to the existing browser using `browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')`.
  - Use **native Playwright methods** (`page.fill()`, `page.locator().click(force=True)`, `page.keyboard.press()`) instead of JavaScript DOM manipulation (`page.evaluate()`) to bypass synthetic event blockers.
  - Run the script over SSH from the headless server: `ssh gateman@100.115.214.26 'cd ~/projects/openclaw-stealth-agents && .venv/bin/python your_script.py'`

### CSDN Automated Publishing (Playwright + X11 Clipboard Bypass)
- **Use Case**: Automatically publishing or editing Markdown articles on CSDN. CSDN's frontend (CodeMirror) intercepts standard Playwright `insert_text()` and strips `\n` newlines, causing format collapse. This skill bypasses it by mimicking a real user's OS-level paste (`Ctrl+V`).
- **Target Machine**: Radxa Moon (`100.115.214.26` with XRDP+XFCE4).
- **Prerequisites**: 
  - `xclip` installed (`sudo apt-get install xclip`).
  - Target Chrome running with `--remote-debugging-port=9222` on `DISPLAY=:10.0`.
- **Core Workflow**:
  1. **Load Clipboard**: Push the local markdown file to the target's system clipboard.
     `ssh gateman@100.115.214.26 "export DISPLAY=:10.0 && cat /tmp/article.md | xclip -selection clipboard"`
  2. **Playwright Execution**:
     - Connect to `http://127.0.0.1:9222`.
     - Navigate to `https://editor.csdn.net/md/` (or `?articleId=XXX` for editing).
     - Focus the editor area: `page.mouse.click(200, 300)`.
     - Clear existing: `page.keyboard.press('Control+A')`, `Backspace`.
     - Paste content: `page.keyboard.press('Control+v')`.
     - Trigger Publish: `page.get_by_role("button", name="发布文章")`.
- **Note**: Always allow `page.wait_for_timeout(3000)` after `Ctrl+v` because CSDN's Markdown parser needs time to render the pasted text before you can safely hit publish.

### Ultra-Stealth Native Browser Hijacking (X11 + Scrot) for Boss直聘
- **Use Case**: Bypassing extreme anti-bot systems (like Boss Zhipin) that detect `--remote-debugging-port` or CDP connections and block rendering (showing a blank white screen) if CDP is active.
- **Methodology**: "Physical/OS-level UI Interaction". Completely abandon Playwright and CDP debugging. Use pure native browser startup + OS-level X11 tools to see and interact.
- **Target Machine**: Radxa Moon (`100.115.214.26` with XRDP+XFCE4).
- **Core Workflow**:
  1. **Clean Start**: Kill existing browsers and remove lock files. Start Chromium purely natively (no debugging ports):
     `ssh gateman@100.115.214.26 "export DISPLAY=:10.0 && killall -9 chromium 2>/dev/null; rm -f ~/.config/chromium/SingletonLock; nohup chromium --start-maximized 'https://login.zhipin.com' > /tmp/chrome.log 2>&1 &"`
  2. **Visual Feedback (Screenshots)**: Wait for load, then use X11 screenshot tool `scrot` to capture the virtual display:
     `ssh gateman@100.115.214.26 "export DISPLAY=:10.0 && scrot -z /tmp/screenshot.png"`
  3. **Interaction (If needed)**: Use `xdotool` to simulate physical mouse clicks and keyboard typing based on coordinates derived from the screenshot.

### Prompt Magic: Professional Architecture Diagrams (Draw.io Style)
- **Use Case**: When the boss asks for a software architecture diagram (e.g., K8s, Cloud architecture) that looks professional, like it was drawn in Draw.io or Lucidchart, instead of a standard AI-art illustration.
- **Base Prompt Template**:
  ```text
  A pristine, professional enterprise software architecture diagram of [SYSTEM/COMPONENTS], designed in the exact style of a clean draw.io or Lucidchart schematic. Flat vector graphics, 2D block diagram, crisp thin lines. The diagram visually maps [LOGICAL FLOW/CONNECTIONS]. High-quality technical aesthetic, using a consistent tech color palette (blues, greens, light grays), neatly aligned boxes, standard tech icons, directional arrows for traffic flow, pure white background, highly detailed, text is clearly readable, masterpiece.
  ```
- **Execution Tool**: Gemini Image Remix script (`gemini-3-pro-image-preview`) or Nano Banana with `--aspect-ratio "16:9"`.


### SSH Internal Network & Jump Host (Bastion) Topology
- **Tailscale Network**: Bound to `gateman56@gmail.com`
- **GCP Client (Alice)**: `tf-vpc0-subnet0-openclaw` (IP: `100.94.13.17`)
- **Moon (Jump Host / Bastion)**: `radxa-cubie-a7a` (Tailscale IP: `100.115.214.26`, Local IP: `10.0.1.105`). SSH user: `gateman`. 
  - Allows public key access from Alice (GCP).
- **Starfive (星光板)**: RISC-V board (Local IP: `10.0.1.227`). SSH user: `gateman`.
  - Trust established from Moon. Accessible via `ssh gateman@10.0.1.227` directly from Moon without password.
- **Nova (Intel NUC / WSL2)**: Win10 NUC running WSL2 (Local IP: `10.0.1.223`). SSH port: `2223`. SSH user: `gateman`. Pass: `32565624`.
  - Headless environment (WSL). Any GUI/Browser tasks requested by Nova must be executed remotely on Moon (`10.0.1.105`).
- **NixOS Laptop (gateman-nix)**: NixOS laptop (Tailscale IP: `100.124.219.42`, Local IP: `10.0.1.3`). SSH user: `gateman`.
  - Accessible via SSH without password from Moon via both LAN and Tailscale.
- **Main PC (AMD Ryzen 7 5800H)**: Boss's primary working machine (Local IP: `10.0.1.173`). SSH user: `gateman`. Pass: `32565624`.
  - Accessible from Moon (or Alice via Moon Jump Host) using PubKey without password.
- **Connection Route from outside**: GCP -> (Tailscale) -> Moon (`100.115.214.26`) -> (Local LAN) -> Starfive (`10.0.1.227`) / Nova (`10.0.1.223:2223`) / NixOS Laptop (`10.0.1.3`) / Main PC (`10.0.1.173`).
- **Login to Alice (GCP)**: Use local key `~/.ssh/gcp_temp` (e.g., `ssh -i ~/.ssh/gcp_temp gateman@100.94.13.17`) if gcloud is missing.

### AList Cloud Drive Management
- **Host**: Starfive RISC-V Board (`10.0.1.227`)
- **Admin Account**: `gateman` / `32565624`
- **Purpose**: Used for managing and aggregating various cloud drives (like Quark Netdisk).
- **Skill**: `alist-quark-cookie-updater` (Located in `skills/alist-quark-cookie-updater/`)
  - **Usage**: Automatically extracts Quark cookie via CDP from local GUI host (Radxa) and updates the AList server via its API to keep the connection alive.


### Downloading Large Files / ISOs (aria2c)
- **Constraint**: GCP (Alice) has limited disk space and bandwidth restrictions. **DO NOT** download large files (ISOs, movies, etc.) locally on GCP.
- **Execution**: Always route heavy downloads to the Starfive board (`10.0.1.227`) using `aria2c`.
- **Command Structure**: Since Starfive is on the LAN, you must jump through Moon (`100.115.214.26`).
  ```bash
  ssh -J gateman@100.115.214.26 gateman@10.0.1.227 'aria2c "<URL>" -d /home/gateman/downloads'
  ```
