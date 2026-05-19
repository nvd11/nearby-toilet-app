from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
            page = browser.new_page()
        except Exception as e:
            print(f"Error: {e}")
            return

        page.goto('https://lowendbox.com/category/special-offers/', timeout=60000)
        page.wait_for_load_state('networkidle')
        
        # Dump all text
        text = page.inner_text('body')
        print(text[:2000])

        browser.close()

if __name__ == "__main__":
    run()
