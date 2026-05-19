# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

- **Oracle ARM VM Polling Status**: Check if `/home/gateman/.openclaw/workspace/success_launch.log` exists. If it does, the 4-core 24GB ARM machine has been successfully created! Notify Jason (Boss) immediately with the good news and stop the polling script if it's still running. If not created yet, briefly check the last few lines of `/home/gateman/.openclaw/workspace/poll_arm.log` to ensure it's still polling normally, but DO NOT alert unless there is a fatal error.

- **Oracle AMD VM Creation**: Run `bash /home/gateman/.openclaw/workspace/try_amd.sh` every 90 minutes to try to create a free-tier AMD VM (VM.Standard.E2.1.Micro). You can use `memory/amd_vm_check_state.json` to keep track of when you last checked, so you only execute the script once every 90 minutes. If it succeeds (returns instance JSON), let Jason know immediately! If it returns Out of capacity or similar, just keep quiet and try again in 90 minutes.
