from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        context = browser.contexts[0]
        
        target_page = None
        for page in context.pages:
            print(f"Tab Title: {page.title()}, URL: {page.url}")
            if 'zhipin' in page.url or 'boss' in page.title().lower():
                target_page = page
                break
                
        if target_page:
            print("Found Zhipin tab! Taking screenshot...")
            target_page.bring_to_front()
            target_page.screenshot(path='/tmp/zhipin_existing.png')
            print("Screenshot saved.")
        else:
            print("Could not find Zhipin tab.")

if __name__ == '__main__':
    run()
