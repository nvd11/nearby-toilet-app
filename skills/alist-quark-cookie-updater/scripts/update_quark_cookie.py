import json
import subprocess
from playwright.sync_api import sync_playwright

def get_cookie():
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
            quark_context = None
            for context in browser.contexts:
                for page in context.pages:
                    if 'quark.cn' in page.url:
                        quark_context = context
                        break
                if quark_context:
                    break
            
            if quark_context:
                cookies = quark_context.cookies()
                cookie_string = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
                return cookie_string
            else:
                return None
    except Exception as e:
        print(f"Failed to extract cookie via Playwright/CDP: {e}")
        return None

def push_to_alist(cookie):
    payload = {
        "id": 1,
        "mount_path": "/Quark",
        "order": 0,
        "driver": "Quark",
        "cache_expiration": 30,
        "sync_timeout": 120,
        "web_proxy": True,
        "webdav_policy": "native_proxy",
        "down_proxy_url": "",
        "down_proxy_sign": True,
        "extract_folder": "",
        "remark": "",
        "disabled": False,
        "addition": json.dumps({
            "cookie": cookie,
            "root_folder_id": "0",
            "order_by": "none",
            "order_direction": "asc",
            "use_transcoding_address": False,
            "only_list_video_file": False,
            "AdditionVersion": 2
        })
    }

    # Save payload locally
    with open('/tmp/quark_update.json', 'w') as f:
        json.dump(payload, f)

    # SCP to Starfive and update via AList API
    bash_script = """
    scp /tmp/quark_update.json gateman@10.0.1.227:~/quark_update.json
    ssh gateman@10.0.1.227 "TOKEN=\\$(curl -s -X POST -d '{\\"username\\":\\"gateman\\",\\"password\\":\\"32565624\\"}' -H 'Content-Type: application/json' http://127.0.0.1:5244/api/auth/login | grep -o '\\"token\\":\\"[^\\"]*\\"' | cut -d'\\"' -f4) && curl -s -X POST -H 'Content-Type: application/json' -H \\"Authorization: \\$TOKEN\\" -d @quark_update.json http://127.0.0.1:5244/api/admin/storage/update && rm ~/quark_update.json"
    """
    
    process = subprocess.run(bash_script, shell=True, capture_output=True, text=True)
    print("AList Update Output:", process.stdout)
    if process.stderr:
        print("AList Update Error:", process.stderr)

if __name__ == '__main__':
    print("Extracting Quark Cookie from local Chromium (Radxa)...")
    cookie = get_cookie()
    if cookie:
        print("Cookie found! Pushing to AList on Starfive (10.0.1.227)...")
        push_to_alist(cookie)
        print("Done!")
    else:
        print("Failed to find Quark cookie. Is pan.quark.cn open in Chromium?")
