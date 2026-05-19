import urllib.request
import yaml

url = "https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_subscription_num"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        print(content[:200])
except Exception as e:
    print(f"Error: {e}")
