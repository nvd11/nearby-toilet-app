from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
        print(f"Total contexts: {len(browser.contexts)}")
        for i, ctx in enumerate(browser.contexts):
            print(f"Context {i} has {len(ctx.pages)} pages")
            for j, page in enumerate(ctx.pages):
                print(f"  Context {i} Page {j} Title: {page.title()} URL: {page.url}")

if __name__ == '__main__':
    run()
