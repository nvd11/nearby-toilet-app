import json

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

cd_systems = []
mode = None

for line in lines:
    if line.startswith("## ⬆️"):
        mode = "up"
    elif line.startswith("## ⬇️"):
        mode = "down"
    elif line.startswith("| **"):
        if "Connect Direct" in line:
            parts = line.split("|")
            cd_systems.append((parts[1].replace("**", "").strip(), mode))

print("Systems using Connect:Direct:")
for sys, direction in cd_systems:
    print(f"- {sys} (Direction: {direction})")

