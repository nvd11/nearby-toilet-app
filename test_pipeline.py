import yaml
from apache_beam.yaml import yaml_transform

yaml_str = """
pipeline:
  type: chain
  transforms:
    - type: ReadFromCsv
      config:
        path: "gs://foo"
"""

parsed = yaml.safe_load(yaml_str)
print(parsed)

# If it's a full pipeline, we can just extract the pipeline block and dump it back to string
inner_yaml = yaml.dump(parsed['pipeline'])
print("Inner yaml:", inner_yaml)
