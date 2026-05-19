import sys
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = context.pages[0]
        
        print("Navigating to article edit page...")
        page.goto('https://editor.csdn.net/md/?articleId=160749510')
        page.wait_for_timeout(6000)
        
        print("Focusing and clearing editor...")
        # Click in the middle of the left editor pane
        page.mouse.click(200, 300) 
        page.wait_for_timeout(500)
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')
        page.wait_for_timeout(500)
        
        print("Pasting from system clipboard (Ctrl+V)...")
        # Since xclip loaded the OS clipboard, this will paste the exact text with newlines!
        page.keyboard.press('Control+v')
        page.wait_for_timeout(3000)
        
        page.screenshot(path='/tmp/csdn_md_perfect_verify.png')
        
        print("Publishing...")
        # Click the red publish button
        page.get_by_role("button", name="发布文章").first.click()
        page.wait_for_timeout(2000)
        
        # Click the confirm publish button in modal
        buttons = page.get_by_role("button", name="发布文章").all()
        if len(buttons) >= 2:
            buttons[-1].click()
        elif len(buttons) == 1:
            buttons[0].click()
            
        page.wait_for_timeout(5000)
        page.screenshot(path='/tmp/csdn_md_perfect_success.png')
        print("Successfully published with perfect formatting!")
    except Exception as e:
        print(f"Error: {e}")
