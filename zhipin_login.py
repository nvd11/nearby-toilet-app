from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
            context = browser.contexts[0]
            # Use the first page or create a new one
            page = context.pages[0] if context.pages else context.new_page()
            
            print("Navigating to Boss Zhipin login...")
            page.goto('https://www.zhipin.com/web/user/?ka=header-login', timeout=60000)
            page.wait_for_timeout(5000) # Wait a bit for JS to render
            
            print("Taking screenshot...")
            page.screenshot(path='/tmp/zhipin_screenshot.png')
            print("Done.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    run()
