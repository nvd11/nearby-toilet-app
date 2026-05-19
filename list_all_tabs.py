import requests

def run():
    try:
        r = requests.get('http://127.0.0.1:9222/json')
        targets = r.json()
        for t in targets:
            print(f"[{t.get('type')}] Title: {t.get('title')} | URL: {t.get('url')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run()
