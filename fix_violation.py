with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "r") as f:
    content = f.read()

# 1. Revert E2E Auto Testing back to original
old_e2e = "| Auto E2E PyBDD testing case for a use case | **8** | Develop automated end-to-end testing scenarios using PyBDD for a specific business use case. Includes effort for Prod violation fixes. |"
new_e2e = "| Auto E2E PyBDD testing case for a use case | **5** | Develop automated end-to-end testing scenarios using PyBDD for a specific business use case. |"
content = content.replace(old_e2e, new_e2e)

# 2. Insert new section before POC / Spike Tasks
new_section = """### Violation & Cyber Security
| Task Description | SP | Examples / Details |
| :--- | :---: | :--- |
| Fix GCP violation | **TBD** | Resolve and fix GCP production security or infrastructure violations. |

### POC / Spike Tasks"""
content = content.replace("### POC / Spike Tasks", new_section)

with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "w") as f:
    f.write(content)
