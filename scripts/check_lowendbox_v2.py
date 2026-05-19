import asyncio
from playwright.sync_api import sync_playwright
import sys

def run():
    with sync_playwright() as p:
        print("Connecting to local browser on Moon (port 9222)...")
        try:
            browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
            page = browser.new_page()
            print("Successfully connected.")
        except Exception as e:
            print(f"Failed to connect to CDP: {e}")
            return

        print("Navigating to LowEndBox...")
        page.goto('https://lowendbox.com/category/special-offers/', timeout=60000)
        page.wait_for_load_state('networkidle')
        
        # Take a screenshot
        page.screenshot(path='/tmp/lowendbox_deals.png')
        print("Screenshot saved to /tmp/lowendbox_deals.png")
        
        # Extract the deals
        print("--- TOP DEALS FOUND ---")
        deals = page.query_selector_all('article')
        for i, deal in enumerate(deals[:5]):
            title_el = deal.query_selector('h1 a, h2 a')
            if title_el:
                title = title_el.inner_text()
                link = title_el.get_attribute('href')
                print(f"{i+1}. {title}")
                print(f"   URL: {link}")
            else:
                print(f"{i+1}. [Unable to parse title]")
        
        browser.close()

if __name__ == "__main__":
    run()
