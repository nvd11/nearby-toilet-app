import sys
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = context.pages[0]
        
        time.sleep(5)
        page.screenshot(path='/tmp/csdn_success2.png')
        print(f"Current URL: {page.url}")
        print("Success publish check")
    except Exception as e:
        print(f"Error: {e}")
