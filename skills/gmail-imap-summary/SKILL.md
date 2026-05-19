---
name: gmail-imap-summary
description: Uses IMAP with a Google App Password to fetch and summarize daily emails in the background. Stable, no browser UI or CAPTCHAs required. Use when the user wants to check their email or get a daily summary.
allowed-tools: Bash(python3:*)
---

# Gmail IMAP Summary Skill

This skill provides a rock-solid, browser-free method for fetching and summarizing emails using IMAP and Google App Passwords.

## Usage

When the user requests an email check or a daily email summary, run the Python script `daily_email_report.py`.

```bash
python3 /home/gateman/.openclaw/workspace/skills/gmail-imap-summary/daily_email_report.py
```

It outputs the latest emails received today. You can then parse the output and present a beautiful, summarized daily report to the user.

## Files

- `fetch_emails.py`: Fetches the last 5 emails (for quick recent checks).
- `daily_email_report.py`: Fetches all emails received today and provides a structured overview.

## Setup & Maintenance

- **Account**: `gateman56@gmail.com`
- **Authentication**: Uses a Google App Password (`lekzjeuykwytooxj`), which bypasses all robot detection and 2FA prompts for background automated access.
- **Server**: `imap.gmail.com` (SSL, Port 993)

If the credentials ever change, update the variables inside the Python scripts.

## Cron Job

A cron job named `daily-email-summary` runs this automatically at 9:00 AM every day and announces the results.