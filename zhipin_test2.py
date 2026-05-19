from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = context.new_page()
        
        print("Navigating to Baidu...")
        page.goto('https://www.baidu.com', timeout=60000)
        page.wait_for_load_state('networkidle')
        print("Baidu Title:", page.title())
        
        print("Navigating to Zhipin...")
        page.goto('https://www.zhipin.com/web/user/?ka=header-login', timeout=60000)
        page.wait_for_timeout(5000)
        print("Zhipin Title:", page.title())
        print("Zhipin Content length:", len(page.content()))
        
        page.screenshot(path='/tmp/zhipin_test2.png')
        page.close()

if __name__ == '__main__':
    run()
