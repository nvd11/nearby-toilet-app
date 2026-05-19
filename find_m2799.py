import os
import json
import base64
import urllib.request

api_key = "AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

def find_in_image(img_path, prompt):
    with open(img_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")
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
            print(f"[{os.path.basename(img_path)}]:", res['candidates'][0]['content']['parts'][0]['text'])
    except Exception as e:
        print(e)

prompt = "Locate the text 'M2799' or 'M2799 Financial Crime' in the image. If found, describe exactly where it is located. If NOT FOUND, say 'NOT FOUND'."

find_in_image("/home/gateman/.openclaw/workspace/cdr-demise-docs/images/CDR_Architecture_Diagram.jpg", prompt)
find_in_image("/home/gateman/.openclaw/workspace/cdr-demise-docs/images/notfull_downstream_list.jpg", prompt)

