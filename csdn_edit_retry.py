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
        
        # We notice the left pane might have been empty in the screenshot.
        # Let's use page.evaluate to set the editor value directly via local storage or by finding the CodeMirror instance
        # Actually, simpler: we can just focus the editor more reliably
        page.goto('https://editor.csdn.net/md/?articleId=160749510')
        page.wait_for_timeout(6000)
        
        # Click exactly in the middle of the left editor pane
        page.mouse.click(200, 300) 
        page.wait_for_timeout(500)
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')
        page.wait_for_timeout(500)
        
        print("Pasting...")
        content = get_content()
        # Fallback to insert_text if clipboard failed in X11
        page.keyboard.insert_text(content)
        page.wait_for_timeout(3000)
        
        page.screenshot(path='/tmp/csdn_md_edit_verify2.png')
        
        # Publish
        page.get_by_role("button", name="发布文章").first.click()
        page.wait_for_timeout(2000)
        
        buttons = page.get_by_role("button", name="发布文章").all()
        if len(buttons) >= 2:
            buttons[-1].click()
        elif len(buttons) == 1:
            buttons[0].click()
            
        page.wait_for_timeout(5000)
        page.screenshot(path='/tmp/csdn_md_edit_success2.png')
        print("Success publish retry")
    except Exception as e:
        print(f"Error: {e}")
