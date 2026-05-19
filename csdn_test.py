import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        
        page.goto('https://editor.csdn.net/md/')
        page.wait_for_timeout(5000)
        page.screenshot(path='/tmp/csdn_editor.png')
        print("Success")
    except Exception as e:
        print(f"Error: {e}")
