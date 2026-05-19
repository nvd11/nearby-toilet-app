from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9224")
    page = None
    for pg in browser.contexts[0].pages:
        if "zhipin.com" in pg.url:
            page = pg
            break
    
    if page:
        print("URL:", page.url)
        # Try to find '个人优势'
        elements = page.locator("text=个人优势").all()
        for i, el in enumerate(elements):
            try:
                parent = el.locator("xpath=../..").inner_html()
                print(f"--- Element {i} Parent HTML ---")
                print(parent[:500]) # Print first 500 chars to avoid huge logs
            except Exception as e:
                pass
