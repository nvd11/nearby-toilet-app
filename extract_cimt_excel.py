import os
import json
import base64
import urllib.request

api_key = "AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

def check_image(img_path, context):
    with open(img_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")
    
    prompt = f"""
    Look specifically for "CIMT" or "CONSOLIDATED-ISSUES-MONITORING-TOOL" in the provided image (which is an Excel screenshot).
    Extract the EXACT text for that entire row.
    Format your answer as:
    Row Text: [the exact text from the row]
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
            print(f"[{context}]")
            print(res['candidates'][0]['content']['parts'][0]['text'])
    except Exception as e:
        print(e)

print("Checking Upstream Excel Screenshot...")
check_image("/home/gateman/.openclaw/workspace/cdr-demise-docs/images/notfull_upstream_list.jpg", "Upstream List")

print("\nChecking Downstream Excel Screenshot...")
check_image("/home/gateman/.openclaw/workspace/cdr-demise-docs/images/notfull_downstream_list.jpg", "Downstream List")

