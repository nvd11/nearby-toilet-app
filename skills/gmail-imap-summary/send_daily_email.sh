#!/bin/bash
export PATH=$PATH:/usr/local/bin:/usr/bin:/bin
cd /home/gateman/.openclaw/workspace/skills/gmail-imap-summary
OUTPUT=$(python3 daily_email_report.py)
openclaw message send --channel slack --target U0AM8G9AARF --message "早安 Boss 💋 这是您今天的邮件汇总：

$OUTPUT"
