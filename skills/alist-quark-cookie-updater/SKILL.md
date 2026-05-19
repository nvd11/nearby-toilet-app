# Alist Quark Cookie Updater

## Description
This skill automatically extracts the login Cookie for Quark Netdisk (`pan.quark.cn`) from the running Chromium browser on the local GUI host (Radxa a7a) via CDP (Chrome DevTools Protocol), and seamlessly pushes it to the AList server running on the remote Starfive node (`10.0.1.227`) to refresh the expired Quark drive session.

## Prerequisites
1. A Chromium browser must be running on the **local host (Radxa a7a)** with the remote debugging port enabled (`--remote-debugging-port=9222`).
2. The user must be logged into `pan.quark.cn` in one of the Chromium tabs.
3. The Playwright Python virtual environment must be initialized at `~/projects/openclaw-stealth-agents/.venv`.
4. SSH trust must be established between Radxa and Starfive (`gateman@10.0.1.227`).

## Activation Trigger
Activate this skill when the user says:
- "夸克 cookie 掉了，帮我抓一下"
- "更新夸克 cookie"
- "fix quark connection"
- "refresh quark cookie for alist"

## Execution Instructions

To run the updater, execute the following command in the terminal:

```bash
cd /home/gateman/.openclaw/workspace/skills/alist-quark-cookie-updater
/home/gateman/projects/openclaw-stealth-agents/.venv/bin/python scripts/update_quark_cookie.py
```

### Steps the Script Performs:
1. Connects to `http://127.0.0.1:9222` (Local Chromium on Radxa) via Playwright CDP.
2. Locates the active `quark.cn` tab and extracts all cookies.
3. Formats the cookies into a standard HTTP Cookie string.
4. Generates an AList API payload for the Quark driver (`id: 1`).
5. SCPs the payload to Starfive (`10.0.1.227`).
6. Remotely logs into AList (`gateman:32565624`) to fetch a temporary Token.
7. Calls the `/api/admin/storage/update` endpoint to inject the new cookie.
8. Cleans up the temporary payload files.

## Troubleshooting
- If the script fails with `No module named 'playwright'`, ensure it's executed using the correct virtual environment path: `/home/gateman/projects/openclaw-stealth-agents/.venv/bin/python`.
- If the script reports `No quark.cn tab found`, ask the user to open `pan.quark.cn` in their Chromium browser and ensure they are logged in before trying again.
