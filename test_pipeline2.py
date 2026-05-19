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

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
options = PipelineOptions()
with beam.Pipeline(options=options) as p:
    # If the user passes 'pipeline:', we can just pass the inner part to YamlTransform
    p | yaml_transform.YamlTransform(yaml.dump(parsed.get('pipeline', parsed)))

