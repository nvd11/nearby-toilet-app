import json
import subprocess
import urllib.request
import urllib.error
import time

token_cmd = subprocess.run(["gcloud", "auth", "print-identity-token"], capture_output=True, text=True, check=True)
token = token_cmd.stdout.strip()

yaml_str = """pipeline:
  type: chain
  transforms:
    - type: Create
      config:
        elements: ["hello", "world"]
    - type: LogForTesting
options:
  subnetwork: "regions/europe-west2/subnetworks/tf-vpc0-subnet0"
"""

payload = {
    "yaml_config": yaml_str,
    "project": "jason-hsbc",
    "region": "europe-west2",
    "temp_location": "gs://jason-hsbc-dataflow/temp",
    "service_account_email": "terraform@jason-hsbc.iam.gserviceaccount.com",
    "job_name": f"yaml-trigger-test-{int(time.time())}"
}

data = json.dumps(payload).encode("utf-8")
url = "https://beam-yaml-orchestrator-912156613264.europe-west2.run.app/trigger"
req = urllib.request.Request(url, data=data, headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
})

try:
    print(f"Triggering Dataflow job (name: {payload['job_name']})...")
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        print("Success! Response:", result)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    print(e.read().decode("utf-8"))
