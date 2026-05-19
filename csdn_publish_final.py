import sys
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = context.pages[0]
        
        # Click the final publish button in the modal
        buttons = page.get_by_role("button", name="发布文章").all()
        if len(buttons) >= 2:
            buttons[-1].click()
            print("Clicked the final publish button")
        else:
            print(f"Found {len(buttons)} buttons, clicking the last one anyway")
            buttons[-1].click()
            
        time.sleep(3)
        page.screenshot(path='/tmp/csdn_success.png')
        print("Success publish")
    except Exception as e:
        print(f"Error: {e}")
