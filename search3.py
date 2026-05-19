import urllib.request
import json

url = 'https://us-central1-aiplatform.googleapis.com/$discovery/rest?version=v1beta1'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    discovery = json.loads(response.read().decode())

def find_ops(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "operations":
                print("Found operations at:", path + ".operations")
            elif isinstance(v, (dict, list)):
                find_ops(v, path + "." + k)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            find_ops(item, path + f"[{i}]")

find_ops(discovery.get("resources", {}).get("projects", {}).get("resources", {}).get("locations", {}).get("resources", {}).get("publishers", {}).get("resources", {}).get("models", {}))
