from playwright.sync_api import sync_playwright
from playwright_stealth import stealth
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        # Use the first tab so the Boss can see it live on his physical screen
        page = context.pages[0] if context.pages else context.new_page()
        
        page.bring_to_front()
        stealth(page)
        
        print("Navigating to Zhipin...")
        page.goto('https://www.zhipin.com/web/user/?ka=header-login', timeout=60000)
        page.wait_for_timeout(5000)
        print("Title:", page.title())
        print("Content length:", len(page.content()))
        
        page.screenshot(path='/tmp/zhipin_stealth2.png')

if __name__ == '__main__':
    run()
