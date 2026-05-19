import urllib.request
import yaml

url = "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Splitted-By-Protocol/vless.yaml"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        data = yaml.safe_load(content)
        if 'proxies' in data:
            print(f"Found {len(data['proxies'])} proxies")
except Exception as e:
    print(f"Error: {e}")
