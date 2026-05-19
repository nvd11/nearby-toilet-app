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
        
        # Extract the latest 10 deals with their summaries
        deals = []
        articles = page.query_selector_all('article')
        for article in articles[:10]:
            title_el = article.query_selector('h1 a, h2 a')
            if title_el:
                title = title_el.inner_text()
                link = title_el.get_attribute('href')
                summary_el = article.query_selector('.entry-content p, .post-content p')
                summary = summary_el.inner_text() if summary_el else ""
                deals.append({"title": title, "link": link, "summary": summary})
        
        for i, deal in enumerate(deals):
            print(f"DEAL {i+1}: {deal['title']}")
            print(f"LINK: {deal['link']}")
            print(f"SUMMARY: {deal['summary'][:200]}...")
            print("-" * 20)

        browser.close()

if __name__ == "__main__":
    run()
