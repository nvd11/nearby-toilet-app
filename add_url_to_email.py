import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/EMAIL_DRAFT_TO_MONA_AJIT.md"
with open(md_path, "r") as f:
    content = f.read()

# Update Ajit section
content = content.replace(
    "**@Ajit** - Could you please review the attached inventory and help clarify/fill in the remaining gaps?",
    "**@Ajit** - Could you please review the consolidated inventory table here: `[Link to INTEGRATIONS.md/Confluence]` and help clarify/fill in the remaining gaps?"
)

# Update Mona section
content = content.replace(
    "I will share the plan document shortly for your review.",
    "You can review the initial draft of the Migration Strategy Plan here: `[Link to CDR_DEMISE_STRATEGY_PLAN.md/Confluence]`."
)

with open(md_path, "w") as f:
    f.write(content)

