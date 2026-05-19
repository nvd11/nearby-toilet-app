import urllib.request
import urllib.parse
import json

url = 'https://us-central1-aiplatform.googleapis.com/$discovery/rest?version=v1'
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    discovery = json.loads(response.read().decode())
    
# look for operations
def find_ops(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "operations":
                print("Found operations at:", prefix)
            find_ops(v, prefix + "." + k)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            find_ops(item, prefix + f"[{i}]")

find_ops(discovery)
