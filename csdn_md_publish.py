import sys
import time
from playwright.sync_api import sync_playwright

def get_content():
    with open('/tmp/csdn_blog_content.md', 'r', encoding='utf-8') as f:
        return f.read()

with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = context.pages[0]
        
        # 1. Fill Title
        page.mouse.click(400, 30) # Click title bar
        page.wait_for_timeout(500)
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')
        page.keyboard.type("放弃 Selenium 吧，Playwright 才是现代自动化爬虫的终极杀器")
        
        # 2. Fill Markdown Editor
        page.mouse.click(200, 300) # Click left editor pane
        page.wait_for_timeout(500)
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')
        page.wait_for_timeout(500)
        page.keyboard.insert_text(get_content())
        page.wait_for_timeout(2000)
        
        page.screenshot(path='/tmp/csdn_md_verify.png')
        
        # 3. Publish
        # Click the red publish button at the bottom right
        page.get_by_role("button", name="发布文章").click()
        page.wait_for_timeout(2000)
        
        page.screenshot(path='/tmp/csdn_md_modal.png')
        
        # Click the final publish button in the modal
        buttons = page.get_by_role("button", name="发布文章").all()
        if len(buttons) >= 2:
            buttons[-1].click()
        elif len(buttons) == 1:
            buttons[0].click()
            
        page.wait_for_timeout(5000)
        page.screenshot(path='/tmp/csdn_md_success.png')
        print("Success publish using MD")
    except Exception as e:
        print(f"Error: {e}")
