with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

old_line = "| **5. Beam Pipeline (Dataflow)** | Develop Beam Pipeline with Pub/Sub IO connector to stream events and write to BigQuery staging data layer. | 5.0 |"
new_line = "| **5. Beam Pipeline (Dataflow)** | Develop Beam Pipeline with Pub/Sub IO connector to stream data from Pub/Sub subscriptions to BigQuery staging layer. | 5.0 |"

content = content.replace(old_line, new_line)

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
