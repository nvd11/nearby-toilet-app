from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        
        for i, page in enumerate(context.pages):
            print(f"Tab {i} Title: {page.title()}, URL: {page.url}")
            page.bring_to_front()
            page.screenshot(path=f'/tmp/tab_{i}.png')

if __name__ == '__main__':
    run()
