from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    print("Connecting to Windows Chrome over CDP...")
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9224")
    context = browser.contexts[0]
    page = context.new_page()
    print("Navigating to BOSS Zhipin login page...")
    page.goto("https://www.zhipin.com/web/user/?ka=header-login", timeout=60000)
    print("Page opened! Disconnecting CDP...")
    browser.disconnect()
