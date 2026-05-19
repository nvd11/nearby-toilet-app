import json
import base64
import subprocess
import urllib.request
import urllib.error
import time

# Create a small valid test file for e2e validation
filename = f"test-real-{int(time.time())}.csv"
local_file = f"/tmp/{filename}"
with open(local_file, "w") as f:
    f.write("id,name\n1,jason\n2,boss")

# Upload the file manually so that it exists in the landing bucket for reading
subprocess.run(["gcloud", "storage", "cp", local_file, f"gs://etl-landing-bucket-poc-e75a1499/{filename}"], check=True)

gcs_event_payload = {
    "kind": "storage#object",
    "name": filename,
    "bucket": "etl-landing-bucket-poc-e75a1499",
    "generation": "1774723144",
    "metageneration": "1",
    "contentType": "text/csv",
    "timeCreated": "2026-03-28T18:39:04.123Z",
    "updated": "2026-03-28T18:39:04.123Z",
    "storageClass": "STANDARD",
    "size": "34"
}

# Base64 encode the payload to match Pub/Sub wrapper
gcs_event_json = json.dumps(gcs_event_payload)
gcs_event_b64 = base64.b64encode(gcs_event_json.encode("utf-8")).decode("utf-8")

pubsub_message = {
    "message": {
        "data": gcs_event_b64,
        "messageId": "1234567890",
        "publishTime": "2026-03-28T18:39:04.123Z"
    },
    "subscription": "projects/jason-hsbc/subscriptions/cloudrun-push-sub-poc"
}

# Retrieve the active Cloud Run URL dynamically
service_url_cmd = subprocess.run(["gcloud", "run", "services", "describe", "etl-orchestrator-svc-poc", "--region=europe-west2", "--format=value(status.url)"], capture_output=True, text=True, check=True)
url = f"{service_url_cmd.stdout.strip()}/pubsub"

# Retrieve an identity token for authentication
token_cmd = subprocess.run(["gcloud", "auth", "print-identity-token"], capture_output=True, text=True, check=True)
token = token_cmd.stdout.strip()

req = urllib.request.Request(url, data=json.dumps(pubsub_message).encode("utf-8"), headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}, method="POST")

print(f"Triggering Webhook for Pub/Sub Event (File: {filename})...")
try:
    with urllib.request.urlopen(req) as response:
        result = response.read().decode("utf-8")
        print(f"Success! Webhook Response: {result}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
