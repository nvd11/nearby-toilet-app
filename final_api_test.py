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
        elements: ["hello", "world", "final-api-test"]
    - type: LogForTesting
options:
  subnetwork: "regions/europe-west2/subnetworks/tf-vpc0-subnet0"
"""

job_name = f"yaml-final-api-test-{int(time.time())}"
payload = {
    "yaml_config": yaml_str,
    "project": "jason-hsbc",
    "region": "europe-west2",
    "temp_location": "gs://jason-hsbc-dataflow/temp",
    "service_account_email": "terraform@jason-hsbc.iam.gserviceaccount.com",
    "job_name": job_name
}

data = json.dumps(payload).encode("utf-8")
url = "https://beam-yaml-orchestrator-912156613264.europe-west2.run.app/trigger"
req = urllib.request.Request(url, data=data, headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
})

print(f"Triggering API for Dataflow job: {job_name} ...")
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        print("API Response:", json.dumps(result, indent=2))
        
        # Wait a moment for Dataflow job to register
        print("\nWaiting for Dataflow job to register...")
        time.sleep(15)
        
        list_cmd = subprocess.run([
            "gcloud", "dataflow", "jobs", "list", 
            "--region=europe-west2", 
            "--project=jason-hsbc", 
            "--limit=1",
            "--format=json"
        ], capture_output=True, text=True, check=True)
        
        jobs = json.loads(list_cmd.stdout)
        if jobs:
            latest_job = jobs[0]
            print(f"\nFound Latest Dataflow Job:")
            print(f"  ID: {latest_job.get('id')}")
            print(f"  Name: {latest_job.get('name')}")
            print(f"  State: {latest_job.get('currentState')}")
            print(f"  Create Time: {latest_job.get('createTime')}")
            if latest_job.get('name') == job_name:
                print("\n✅ Verification Successful: Job name matches perfectly!")
            else:
                print("\n⚠️ Warning: Latest job name doesn't match expected. It might still be queuing.")
        else:
            print("\nNo jobs found in the region.")

except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    print(e.read().decode("utf-8"))
