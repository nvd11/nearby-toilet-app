import time
from playwright.sync_api import sync_playwright
text_to_fill = "test"
try:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9224")
        context = browser.contexts[0]
        target_page = None
        for page in context.pages:
            if "zhipin.com" in page.url and "resume" in page.url:
                target_page = page
                break
        if not target_page:
            print("No zhipin resume page found in these URLs:")
            for page in context.pages:
                print(" -", page.url)
            exit(1)
        print("Found target page:", target_page.url)
        target_page.bring_to_front()
except Exception as e:
    print("Error:", e)
