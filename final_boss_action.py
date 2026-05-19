import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9224")
    context = browser.contexts[0]
    page = context.pages[0]
    
    # 既然 Boss 已经开了这个窗口，我们直接用它导航
    print("Navigating the current tab to BOSS Zhipin...")
    try:
        page.goto("https://www.zhipin.com/web/geek/resume", timeout=15000)
    except Exception as e:
        print("Goto timeout/error (often happens if interrupted):", e)
        
    time.sleep(3)
    print("Current URL:", page.url)
    page.screenshot(path="/home/gateman/.openclaw/workspace/boss_current.png")
    print("Screenshot saved to boss_current.png")
