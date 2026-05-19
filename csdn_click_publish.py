import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        
        # Click the "发布文章" button
        page.get_by_role("button", name="发布文章").click()
        page.wait_for_timeout(2000)
        page.screenshot(path='/tmp/csdn_publish_modal.png')
        print("Success modal")
    except Exception as e:
        print(f"Error: {e}")
