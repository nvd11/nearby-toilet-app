import json

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

sftp_count = 0
sftp_systems = []
mode = None

for line in lines:
    if line.startswith("## ⬆️"):
        mode = "up"
    elif line.startswith("## ⬇️"):
        mode = "down"
    elif line.startswith("| **") and mode == "up":
        if "SFTP" in line:
            sftp_count += 1
            parts = line.split("|")
            sftp_systems.append(parts[1].replace("**", "").strip())

print(f"Total Upstream Systems using SFTP: {sftp_count}")
print("Systems:", ", ".join(sftp_systems))

