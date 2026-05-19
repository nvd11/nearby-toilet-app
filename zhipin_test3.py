from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = context.new_page()
        
        print("Navigating to Zhipin Home...")
        response = page.goto('https://www.zhipin.com/', timeout=60000)
        print("Response status:", response.status if response else "No response")
        page.wait_for_timeout(5000)
        print("Zhipin Title:", page.title())
        
        page.screenshot(path='/tmp/zhipin_test3.png')
        page.close()

if __name__ == '__main__':
    run()
