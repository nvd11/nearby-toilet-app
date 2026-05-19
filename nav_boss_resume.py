from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    print("Connecting to Windows Chrome over CDP...")
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9224")
    context = browser.contexts[0]
    
    # Find the zhipin page
    zhipin_page = None
    for page in context.pages:
        if "zhipin.com" in page.url:
            zhipin_page = page
            break
            
    if not zhipin_page:
        zhipin_page = context.new_page()
        
    print("Navigating to Resume page...")
    try:
        zhipin_page.goto("https://www.zhipin.com/web/geek/resume", timeout=15000)
    except Exception as e:
        print("Goto exception (often interrupted by redirect):", e)
        
    zhipin_page.wait_for_timeout(3000)
    print("Current URL:", zhipin_page.url)
    
    # Let's take a screenshot to see where we are
    zhipin_page.screenshot(path="/home/gateman/.openclaw/workspace/boss_resume.png")
    print("Screenshot saved.")
