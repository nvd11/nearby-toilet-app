import urllib.request
import json
try:
    resp = urllib.request.urlopen("http://127.0.0.1:9223/json/version")
    print(resp.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)
