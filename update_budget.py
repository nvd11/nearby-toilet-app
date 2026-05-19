import json
import subprocess
import sys

account_id = "186004631963"
budget_name = "Zero-Spend-Alert"
aws_cmd = ["/home/gateman/.local/bin/aws", "budgets", "describe-budgets", "--account-id", account_id]

# Fetch the existing budget
env_vars = {
    "AWS_ACCESS_KEY_ID": "AKIASWTV5OGNY6BNSZH2",
    "AWS_SECRET_ACCESS_KEY": "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"
}
import os
env = os.environ.copy()
env.update(env_vars)

res = subprocess.run(aws_cmd, env=env, capture_output=True, text=True)
if res.returncode != 0:
    print("Error fetching budgets:", res.stderr)
    sys.exit(1)

data = json.loads(res.stdout)
budgets = data.get("Budgets", [])
if not budgets:
    print("No budgets found.")
    sys.exit(1)

budget = budgets[0]

# Remove read-only fields
keys_to_remove = ["CalculatedSpend", "LastUpdatedTime", "HealthStatus"]
for k in keys_to_remove:
    budget.pop(k, None)

# Update CostTypes to include Credit
budget["CostTypes"]["IncludeCredit"] = True

# Write to a file
with open("new-budget.json", "w") as f:
    json.dump(budget, f)

print("Budget updated locally, executing aws update-budget...")

update_cmd = [
    "/home/gateman/.local/bin/aws", "budgets", "update-budget",
    "--account-id", account_id,
    "--new-budget", "file://new-budget.json"
]

res_update = subprocess.run(update_cmd, env=env, capture_output=True, text=True)
if res_update.returncode != 0:
    print("Error updating budget:", res_update.stderr)
    sys.exit(1)

print("Budget successfully updated!")
