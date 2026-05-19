from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        
        # Bring page to front so boss can see it
        page.bring_to_front()
        
        # Apply stealth
        stealth_sync(page)
        
        print("Navigating to Zhipin...")
        page.goto('https://www.zhipin.com/', timeout=60000)
        page.wait_for_timeout(5000)
        print("Title after stealth:", page.title())
        print("Length:", len(page.content()))
        
        page.screenshot(path='/tmp/zhipin_stealth.png')

if __name__ == '__main__':
    run()
