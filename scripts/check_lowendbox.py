import asyncio
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Use existing browser on Radxa Moon (port 9222) as per TOOLS.md
        try:
            browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
            page = browser.new_page()
            print("Connected to remote browser.")
        except Exception as e:
            print(f"Failed to connect to CDP: {e}")
            print("Starting isolated browser...")
            browser = p.chromium.launch()
            page = browser.new_page()

        page.goto('https://lowendbox.com/category/special-offers/', timeout=60000)
        page.wait_for_load_state('networkidle')
        
        # Take a screenshot to show the Boss
        page.screenshot(path='/tmp/lowendbox_deals.png')
        
        # Extract the deals
        deals = page.query_selector_all('article')
        print("--- TOP DEALS FOUND ---")
        for i, deal in enumerate(deals[:5]):
            title = deal.query_selector('h2').inner_text() if deal.query_selector('h2') else "No Title"
            link = deal.query_selector('h2 a').get_attribute('href') if deal.query_selector('h2 a') else "No Link"
            print(f"{i+1}. {title}")
            print(f"   URL: {link}")
        
        browser.close()

if __name__ == "__main__":
    run()
