import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

up_systems = set()
down_systems = set()
mode = None

# Pass 1: Collect exact system names from both tables
for line in lines:
    if line.startswith("## ⬆️"):
        mode = "up"
    elif line.startswith("## ⬇️"):
        mode = "down"
    elif line.startswith("| **"):
        sys_name = line.split("|")[1].replace("**", "").strip()
        if mode == "up":
            up_systems.add(sys_name)
        elif mode == "down":
            down_systems.add(sys_name)

# Pass 2: Rewrite file with new header and strictly calculated boolean
out = []
mode = None
for line in lines:
    if "Bi-directional?" in line:
        out.append(line.replace("Bi-directional?", "Is Both Upstream & Downstream?"))
    elif line.startswith("## ⬆️"):
        mode = "up"
        out.append(line)
    elif line.startswith("## ⬇️"):
        mode = "down"
        out.append(line)
    elif line.startswith("| **"):
        parts = line.split("|")
        sys_name = parts[1].replace("**", "").strip()
        
        # Recalculate strictly based on intersection
        is_both = (sys_name in up_systems) and (sys_name in down_systems)
        new_val = " ✅ Yes " if is_both else " ❌ No "
        
        parts[4] = new_val
        out.append("|".join(parts))
    else:
        out.append(line)

with open(md_path, "w") as f:
    f.writelines(out)

