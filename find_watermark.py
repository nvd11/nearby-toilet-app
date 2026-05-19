import os
import sys
import base64
import json
import urllib.request

api_key = os.environ.get('GEMINI_API_KEY')
img_path = sys.argv[1]

with open(img_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "contents": [{
        "parts": [
            {"text": "Return the bounding box in [ymin, xmin, ymax, xmax] format for the text '豆包' or 'AI生成' in this image. Only return the bounding box coordinates, nothing else. The coordinates should be normalized from 0 to 1000."},
            {"inlineData": {"mimeType": "image/jpeg", "data": b64}}
        ]
    }]
}

req = urllib.request.Request(
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode("utf-8"))
except Exception as e:
    print("Error:", e)
