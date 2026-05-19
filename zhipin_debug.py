from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else context.new_page()
            
            print("Title:", page.title())
            print("Content length:", len(page.content()))
            print("Taking another screenshot...")
            page.screenshot(path='/tmp/zhipin_debug.png')
            print("Done.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    run()
