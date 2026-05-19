import os
import json
import base64
import urllib.request

api_key = "AIzaSyB2EQmHBevsc_X2THRuDX0UOkUjL_iQfbQ"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

def get_sheet_name(img_path, context):
    with open(img_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode("utf-8")
    
    prompt = f"""
    This is an Excel screenshot ({context}).
    Look at the VERY BOTTOM of the image for the Excel sheet tabs.
    Which sheet tab is currently selected/active (usually highlighted in white or a different color, or has a green underline)?
    Reply with ONLY the exact name of the active sheet tab.
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
            print(f"[{context}] Sheet Name: {res['candidates'][0]['content']['parts'][0]['text'].strip()}")
    except Exception as e:
        print(e)

get_sheet_name("/home/gateman/.openclaw/workspace/cdr-demise-docs/images/notfull_upstream_list.jpg", "Upstream List")
get_sheet_name("/home/gateman/.openclaw/workspace/cdr-demise-docs/images/notfull_downstream_list.jpg", "Downstream List")

