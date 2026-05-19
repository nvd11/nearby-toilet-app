import json
import base64
import subprocess
import urllib.request
import urllib.error
import time

token_cmd = subprocess.run(["gcloud", "auth", "print-identity-token"], capture_output=True, text=True, check=True)
token = token_cmd.stdout.strip()

gcs_event_payload = {
    "kind": "storage#object",
    "name": "test-webhook-again.csv",
    "bucket": "etl-landing-bucket-poc-e75a1499",
}

gcs_event_json_str = json.dumps(gcs_event_payload)
encoded_data = base64.b64encode(gcs_event_json_str.encode("utf-8")).decode("utf-8")

pubsub_envelope = {
    "message": {
        "data": encoded_data,
    },
}

data = json.dumps(pubsub_envelope).encode("utf-8")
url = "https://etl-orchestrator-svc-poc-912156613264.europe-west2.run.app/pubsub"

req = urllib.request.Request(url, data=data, headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
})

try:
    print(f"Triggering Webhook for Pub/Sub Event (File: {gcs_event_payload['name']})...")
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        print("Success! Webhook Response:", json.dumps(result, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    print(e.read().decode("utf-8"))
