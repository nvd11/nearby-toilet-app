import os
import json
import base64
import urllib.request

api_key = "AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

with open("/home/gateman/.openclaw/media/inbound/453449a6-38a2-4ea8-84c7-3570dbde83bb.jpg", "rb") as f:
    img_data = base64.b64encode(f.read()).decode("utf-8")

prompt = """
Extract all the text from this screenshot of meeting minutes.
Then, provide a brief analysis of whether these architectural decisions align well with a migration from an Oracle on-prem database to GCP BigQuery (RCDP).
Focus specifically on the feasibility of the 4 upstream patterns and 3 downstream patterns proposed.
"""

payload = {
    "contents": [{
        "parts": [
            {"inline_data": {"mime_type": "image/jpeg", "data": img_data}},
            {"text": prompt}
        ]
    }]
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode())
        print(res['candidates'][0]['content']['parts'][0]['text'])
except Exception as e:
    print(e)
