import os
import json
import base64
import urllib.request

api_key = "AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

with open("/home/gateman/.openclaw/workspace/cdr-demise-docs/images/CDR_Architecture_Diagram.jpg", "rb") as f:
    img_data = base64.b64encode(f.read()).decode("utf-8")

prompt = """
Look specifically at the "Downstream Systems" section (the right side) of the architecture diagram.
Locate the box labeled "NAS".
1. Are there any arrows pointing OUT of this NAS box to other systems or entities?
2. Does the diagram explicitly list or show WHO or WHICH specific systems read data from this downstream NAS?
Describe exactly what is shown around the downstream NAS box.
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
