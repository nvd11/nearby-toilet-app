import os
import json
import base64
import urllib.request

api_key = "AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

with open("/home/gateman/.openclaw/workspace/cdr-demise-docs/images/CDR_Architecture_Diagram.jpg", "rb") as f:
    img_data = base64.b64encode(f.read()).decode("utf-8")

prompt = """
Here is a list of downstream systems I have identified:
Rapid2, Ask, CIMT, ECM, RegMap, UCM, Breach, Vetting, GPPS, KYE-US-INTERFACE, Hotline, RRIS, SDF, Engage2, Risk Culture Dashboard, ECA, GFHR-INTEG, My trades, PQM, EUC, SUPERVISION, M2799.

Based ON THE IMAGE PROVIDED, which of these specific systems consume data via API? 
List them out and specify what the diagram says about their connection (e.g. 'API', 'REST API', etc.).
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
