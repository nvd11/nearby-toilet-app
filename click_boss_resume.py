from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    print("Connecting to Windows Chrome over CDP...")
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9224")
    context = browser.contexts[0]
    
    zhipin_page = None
    for page in context.pages:
        if "zhipin.com" in page.url:
            zhipin_page = page
            break
            
    if zhipin_page:
        print("Clicking Resume tab...")
        # usually top nav has a link to resume
        zhipin_page.locator("text=简历").first.click(force=True)
        zhipin_page.wait_for_timeout(3000)
        print("Current URL:", zhipin_page.url)
        zhipin_page.screenshot(path="/home/gateman/.openclaw/workspace/boss_resume.png")
        print("Screenshot saved.")
