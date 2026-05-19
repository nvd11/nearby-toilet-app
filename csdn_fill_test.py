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
        page.locator('input[placeholder*="请输入文章标题"]').fill("放弃 Selenium 吧，Playwright 才是现代自动化爬虫的终极杀器")
        
        # 2. Fill Editor
        # Click the left side Markdown editor
        page.locator('.editor').click()
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')
        
        page.keyboard.insert_text(get_content())
        time.sleep(2)
        
        # 3. Click Publish Button
        page.get_by_role("button", name="发布文章").click()
        time.sleep(3)
        
        page.screenshot(path='/tmp/csdn_modal_2.png')
        print("Success fill")
    except Exception as e:
        print(f"Error: {e}")
