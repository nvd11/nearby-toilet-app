import json
import urllib.request
import time

yaml_str = """pipeline:
  type: chain
  transforms:
    - type: Create
      config:
        elements: ["local", "test"]
    - type: LogForTesting
"""

payload = {
    "yaml_config": yaml_str,
    "project": "jason-hsbc",
    "region": "europe-west2",
    "temp_location": "gs://jason-hsbc-dataflow/temp",
    "job_name": "yaml-trigger-local"
}

data = json.dumps(payload).encode("utf-8")
url = "http://localhost:8081/trigger"
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

print("Sending request to local orchestrator...")
start = time.time()
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        duration = time.time() - start
        print(f"Request finished in {duration:.2f} seconds.")
        print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")
