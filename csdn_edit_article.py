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
        
        print("Navigating to edit URL...")
        page.goto('https://editor.csdn.net/md/?articleId=160749510')
        page.wait_for_timeout(6000)
        
        # Click left editor pane
        page.mouse.click(200, 300) 
        page.wait_for_timeout(500)
        page.keyboard.press('Control+A')
        page.keyboard.press('Backspace')
        page.wait_for_timeout(500)
        
        print("Copying to clipboard and pasting...")
        content = get_content()
        page.evaluate('''([text]) => {
            const el = document.createElement('textarea');
            el.value = text;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
        }''', [content])
        
        page.keyboard.press('Control+v')
        page.wait_for_timeout(3000)
        
        page.screenshot(path='/tmp/csdn_md_edit_verify.png')
        print("Pasted. Clicking publish...")
        
        # Click the red publish button at the bottom right
        # Because we are in MD editor, it's usually at the top right or bottom right.
        # Let's just use the role button.
        page.get_by_role("button", name="发布文章").first.click()
        page.wait_for_timeout(2000)
        
        # Click the final publish button in the modal
        buttons = page.get_by_role("button", name="发布文章").all()
        if len(buttons) >= 2:
            buttons[-1].click()
        elif len(buttons) == 1:
            buttons[0].click()
            
        page.wait_for_timeout(5000)
        page.screenshot(path='/tmp/csdn_md_edit_success.png')
        print("Success publish edited article")
    except Exception as e:
        print(f"Error: {e}")
