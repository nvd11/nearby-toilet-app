from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        page = context.new_page()
        
        page.goto('https://www.zhipin.com/', timeout=60000)
        page.wait_for_timeout(3000)
        print(page.content()[:1000])
        page.close()

if __name__ == '__main__':
    run()
