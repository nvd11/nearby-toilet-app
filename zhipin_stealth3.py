from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import time

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
            context = browser.contexts[0]
            # Use the first tab so the Boss can see it live on his physical screen
            page = context.pages[0] if context.pages else context.new_page()
            
            page.bring_to_front()
            
            stealth = Stealth()
            stealth.apply_stealth_sync(page)
            
            print("Navigating to Zhipin...")
            # Going to standard homepage to see if it loads
            response = page.goto('https://www.zhipin.com/', timeout=60000)
            page.wait_for_timeout(5000)
            
            print("Title:", page.title())
            print("Content length:", len(page.content()))
            
            page.screenshot(path='/tmp/zhipin_stealth3.png')
            print("Done.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    run()
