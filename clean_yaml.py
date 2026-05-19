import sys, json
# Fallback if pyyaml is missing: read json, write json, or if we just want to remove managedFields
# Let's try to install python3-yaml just in case
