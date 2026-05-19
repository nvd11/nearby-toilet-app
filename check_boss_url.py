from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9224")
    for ctx in browser.contexts:
        for page in ctx.pages:
            print("URL:", page.url)
