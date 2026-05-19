import sys
import jinja2
from apache_beam.yaml import main as yaml_main

def run():
    yaml_str = """
pipeline:
  type: chain
  transforms:
    - type: ReadFromCsv
      config:
        path: "gs://etl-landing-bucket-poc-e75a1499/test.csv"
    - type: WriteToBigQuery
      config:
        table: "jason-hsbc:etl_poc_dataset.target_users_poc"
        create_disposition: CREATE_IF_NEEDED
        write_disposition: WRITE_APPEND
"""
    
    # We can write the rendered YAML to a temporary file
    temp_yaml_path = "/tmp/rendered_pipeline.yaml"
    with open(temp_yaml_path, "w") as f:
        f.write(yaml_str)

    # Prepare argv for yaml_main
    argv = [
        "--yaml_pipeline_file=" + temp_yaml_path,
        "--runner=DataflowRunner",
        "--project=jason-hsbc",
        "--region=europe-west2",
        "--temp_location=gs://etl-temp-bucket-poc-e75a1499/temp",
        "--service_account_email=dataflow-worker-sa-poc@jason-hsbc.iam.gserviceaccount.com",
        "--subnetwork=regions/europe-west2/subnetworks/subnet-west2",
        "--job_name=native-top-level-yaml-1"
    ]
    
    print("Running with argv:", argv)
    yaml_main.run(argv)

if __name__ == "__main__":
    run()
