import os
import json
import base64
import urllib.request

api_key = "AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

def process_image(img_path, context):
    with open(img_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")
    
    prompt = f"""
    This is an Excel screenshot showing system integrations ({context}).
    For EVERY SINGLE ROW visible in this spreadsheet containing a system acronym in column E or F (like CIMT, UCM, Rapid2, etc.), please extract the SYSTEM NAME and the INTEGRATION METHOD (look for words like File, API, DB, View, MQ, DB Link under the columns roughly labeled 'Interface Type' or 'Data').
    
    Output format should strictly be:
    SYSTEM_NAME: METHOD
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

print("Processing Upstream Excel...")
process_image("/home/gateman/.openclaw/workspace/cdr-demise-docs/images/notfull_upstream_list.jpg", "Upstream List")

print("\nProcessing Downstream Excel...")
process_image("/home/gateman/.openclaw/workspace/cdr-demise-docs/images/notfull_downstream_list.jpg", "Downstream List")

