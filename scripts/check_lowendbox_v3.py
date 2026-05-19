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
        
        # Take a fresh screenshot
        page.screenshot(path='/tmp/lowendbox_final.png')
        
        # Extract the deals - updated selector
        print("--- TOP DEALS FOUND ---")
        articles = page.query_selector_all('div.post-content')
        for i, article in enumerate(articles[:6]):
            title_el = article.query_selector('h1.entry-title a')
            if title_el:
                title = title_el.inner_text()
                link = title_el.get_attribute('href')
                print(f"{i+1}. {title}")
                print(f"   URL: {link}")
                
                # Try to extract a brief summary or price if possible
                summary = article.query_selector('p')
                if summary:
                    print(f"   Summary: {summary.inner_text()[:150]}...")
            else:
                # Fallback for different layout
                title_el = article.query_selector('h2 a')
                if title_el:
                    print(f"{i+1}. {title_el.inner_text()}")
                    print(f"   URL: {title_el.get_attribute('href')}")
        
        browser.close()

if __name__ == "__main__":
    run()
