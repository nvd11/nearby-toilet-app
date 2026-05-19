# Safe Remote Execution (safe-remote-exec)

## Description
Mandatory protocol for running long-lived remote commands (like SSH tunnels, remote browser debugging, Playwright operations, or tailing logs) without locking the OpenClaw conversational channel.

## Trigger
Use this skill whenever the user asks to:
- Connect to a home LAN device via jump host (e.g., `10.0.1.223`, `10.0.1.3`, `10.0.1.227`).
- Run `playwright` or GUI automation on a remote machine.
- Start a long-running process (like Chrome with `--remote-debugging-port`).

## Execution Rules

### 1. ABSOLUTELY NO SYNCHRONOUS LONG SHELL COMMANDS
You are forbidden from using `call:default_api:exec` for blocking SSH sessions or scripts that take more than 5 seconds. If you do, you will crash the Slack channel.

### 2. How to execute instead (Choose A or B):

**Option A: The Background Worker (Preferred for simple long commands)**
Use the `exec` tool but you MUST set `background: true`. 
Example:
`ssh -J gateman@100.115.214.26 gateman@10.0.1.223 'nohup your_long_command > /tmp/out.log 2>&1 &'`

**Option B: Sub-Agent Spawn (Preferred for complex/multi-step interactions)**
If you need to execute a Python Playwright script remotely and react to its output, spawn a sub-agent!
Use `sessions_spawn` with `runtime: "subagent"`, and instruct the subagent to run the script and report back. 
IMMEDIATELY call `sessions_yield` to end your turn after spawning.

### 3. Acknowledgment
Always explicitly tell the user: "我已经根据 \`safe-remote-exec\` 技能的规定，将任务放入后台（或交给子 Agent），保证不会卡死聊天通道！"
