import os
import json
import base64
import urllib.request

api_key = "AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

with open("/home/gateman/.openclaw/workspace/cdr-demise-docs/images/CDR_Architecture_Diagram.jpg", "rb") as f:
    img_data = base64.b64encode(f.read()).decode("utf-8")

prompt = """
Examine the following upstream systems:
CIMT, ABC Register, PGT - HR (HR-SUCCESSFACTORS-CS-EC), GFHR-INTEG, GBM-THOR-US, PHANTOM.
Are any of these visible in the image? If so, what is the exact text on the arrow connecting them to the center?
Also, look closely at the "File Based" arrow. Which systems flow into the "File Based" or "SFTP" arrows?
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
