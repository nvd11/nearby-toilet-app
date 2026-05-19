from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = context.new_page()
        
        print("Navigating to Zhipin...")
        try:
            response = page.goto('https://www.zhipin.com/', timeout=30000)
            print(f"Response status: {response.status if response else 'None'}")
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"Goto error: {e}")
            
        print(f"Current URL: {page.url}")
        print(f"Title: {page.title()}")
        
        page.screenshot(path='/tmp/zhipin_moon2.png')
        print("Screenshot saved.")

if __name__ == '__main__':
    run()
