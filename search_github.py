import urllib.request
import json
import base64

url = "https://api.github.com/search/code?q=predictLongRunning+language:python"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        if 'items' in data and len(data['items']) > 0:
            for item in data['items'][:3]:
                print(item['html_url'])
except Exception as e:
    print(e)
