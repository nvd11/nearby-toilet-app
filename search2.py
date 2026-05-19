import urllib.request
import json

url = 'https://us-central1-aiplatform.googleapis.com/$discovery/rest?version=v1'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    discovery = json.loads(response.read().decode())
    
models_res = discovery.get("resources", {}).get("projects", {}).get("resources", {}).get("locations", {}).get("resources", {}).get("publishers", {}).get("resources", {}).get("models", {})
ops_res = models_res.get("resources", {})
print(json.dumps(ops_res, indent=2))
