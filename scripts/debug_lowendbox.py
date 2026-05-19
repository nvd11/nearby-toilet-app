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
        
        # Debug: List all h1 and h2
        print("--- DEBUG: H1 TAGS ---")
        h1s = page.query_selector_all('h1')
        for h in h1s:
            print(f"H1: {h.inner_text()}")
            
        print("--- DEBUG: H2 TAGS ---")
        h2s = page.query_selector_all('h2')
        for h in h2s:
            print(f"H2: {h.inner_text()}")
            
        # Try to find all links in entry-title
        print("--- DEBUG: ENTRY TITLES ---")
        titles = page.query_selector_all('.entry-title a')
        for t in titles:
            print(f"Title Link: {t.inner_text()} -> {t.get_attribute('href')}")

        browser.close()

if __name__ == "__main__":
    run()
