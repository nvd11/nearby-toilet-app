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
        
        # Use evaluate to get data directly from the DOM
        deals = page.evaluate("""
            () => {
                const results = [];
                const posts = document.querySelectorAll('div.post-content, article');
                posts.forEach(post => {
                    const titleEl = post.querySelector('h1 a, h2 a');
                    const summaryEl = post.querySelector('p');
                    if (titleEl) {
                        results.push({
                            title: titleEl.innerText,
                            link: titleEl.href,
                            summary: summaryEl ? summaryEl.innerText : ""
                        });
                    }
                });
                return results;
            }
        """)
        
        print(f"TOTAL DEALS FOUND: {len(deals)}")
        for i, deal in enumerate(deals[:10]):
            print(f"DEAL {i+1}: {deal['title']}")
            print(f"LINK: {deal['link']}")
            print(f"SUMMARY: {deal['summary'][:150]}...")
            print("-" * 20)

        browser.close()

if __name__ == "__main__":
    run()
