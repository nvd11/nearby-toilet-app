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
        
        # Go to editor page
        page.goto('https://editor.csdn.net/')
        page.wait_for_timeout(3000)
        
        # Find and click "使用 MD 编辑器" button if it exists
        try:
            switch_btn = page.locator('text="使用 MD 编辑器"')
            if switch_btn.is_visible():
                switch_btn.click()
                page.wait_for_timeout(3000)
                print("Switched to MD Editor")
        except Exception as e:
            print("Switch button not found or error:", e)
            
        # Fill Title
        title_input = page.locator('input[placeholder*="文章标题"]')
        title_input.fill("放弃 Selenium 吧，Playwright 才是现代自动化爬虫的终极杀器")
        
        # Try to find the markdown editor input area.
        # In CSDN MD editor, there's usually a .editor class or we can just click the large editor pane.
        # We will try clicking the editor container.
        try:
            editor = page.locator('.editor')
            editor.click()
        except:
            # Fallback: click somewhere in the middle-left of the page
            page.mouse.click(300, 300)
            
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')
        page.wait_for_timeout(500)
        
        # Insert the markdown content
        page.keyboard.insert_text(get_content())
        page.wait_for_timeout(2000)
        
        # Screenshot to verify markdown formatting
        page.screenshot(path='/tmp/csdn_md_verify.png')
        
        # Click the "发布文章" button
        publish_btn1 = page.get_by_role("button", name="发布文章").first
        publish_btn1.click()
        page.wait_for_timeout(2000)
        
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
