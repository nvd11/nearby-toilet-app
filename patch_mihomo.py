import yaml
import sys

def patch_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # The 3 nodes to add
    nodes = [
        {
            "name": "Moon-GCP-Belgium",
            "type": "vless",
            "server": "34.53.168.57",
            "port": 443,
            "uuid": "abe5f7dd-3fc0-4d83-a153-87709875b69a",
            "network": "tcp",
            "tls": True,
            "udp": True,
            "flow": "xtls-rprx-vision",
            "servername": "www.microsoft.com",
            "reality-opts": {
                "public-key": "L1lTxc03C8zOHX-DHjOQ30s3DYGn12aZI6wKvw3bIC0",
                "short-id": "1b2b3c4d5e6f7a8b"
            },
            "client-fingerprint": "chrome"
        },
        {
            "name": "Moon-SG-AWS",
            "type": "vless",
            "server": "13.212.67.185",
            "port": 443,
            "uuid": "abe5f7dd-3fc0-4d83-a153-87709875b69a",
            "network": "tcp",
            "tls": True,
            "udp": True,
            "flow": "xtls-rprx-vision",
            "servername": "www.microsoft.com",
            "reality-opts": {
                "public-key": "L1lTxc03C8zOHX-DHjOQ30s3DYGn12aZI6wKvw3bIC0",
                "short-id": "1b2b3c4d5e6f7a8b"
            },
            "client-fingerprint": "chrome"
        },
        {
            "name": "CF-亚太翻墙神机",
            "type": "vless",
            "server": "vpn.jpgcp.cloud",
            "port": 443,
            "uuid": "28661606-f836-460f-87ad-1b7248a455dc",
            "network": "ws",
            "tls": True,
            "udp": True,
            "sni": "vpn.jpgcp.cloud",
            "client-fingerprint": "chrome",
            "ws-opts": {
                "path": "/?ed=2048",
                "headers": {
                    "Host": "vpn.jpgcp.cloud"
                }
            }
        }
    ]

    # Add to proxies
    existing_proxy_names = {p['name'] for p in data.get('proxies', [])}
    for node in nodes:
        if node['name'] not in existing_proxy_names:
            data['proxies'].insert(0, node) # Add to top

    # Add to proxy-groups
    node_names = [n['name'] for n in nodes]
    for group in data.get('proxy-groups', []):
        if group['name'] in ["赔钱机场", "自动选择", "故障转移"]:
            # insert after "故障转移" or "自动选择" or just at the beginning
            for name in reversed(node_names):
                if name not in group['proxies']:
                    group['proxies'].insert(2 if len(group['proxies']) > 2 else 0, name)

    class CustomDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

    with open('laptop_config_patched.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, Dumper=CustomDumper)

if __name__ == '__main__':
    patch_yaml('laptop_config.yaml')
