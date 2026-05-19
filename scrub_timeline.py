import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_1_YEAR_DEMISE_PLAN.md"
with open(md_path, "r") as f:
    content = f.read()

# Replace all 1-year and month references
content = re.sub(r'Target:\*\* 1-Year Demise Initiative \(Conditional\)', 'Target:** Strategic CDR Decommissioning', content)
content = re.sub(r'aggressive 1-year demise target', 'successful demise target', content)
content = re.sub(r'\(Months 1-3\)', '', content)
content = re.sub(r'\(Months 4-10\)', '', content)
content = re.sub(r'\(Months 11-12\)', '', content)
content = re.sub(r'\(Post 1-Year Target\)', '(Post-Migration)', content)
content = re.sub(r'The "1-Year" Caveats', 'Migration Prerequisites', content)
content = re.sub(r'The 1-year timeline is highly aggressive and', 'The proposed migration timeline is highly aggressive and', content)

with open(md_path, "w") as f:
    f.write(content)

