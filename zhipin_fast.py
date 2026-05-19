from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        try:
            print("Launching Chrome...")
            ctx = p.chromium.launch_persistent_context(
                user_data_dir='/home/gateman/.config/google-chrome',
                headless=False,
                executable_path='/opt/google/chrome/chrome',
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--remote-debugging-port=9222',
                    '--disable-infobars',
                    '--hide-crash-restore-bubble'
                ]
            )
            page = ctx.pages[0] if len(ctx.pages) > 0 else ctx.new_page()
            
            print("Navigating to Zhipin...")
            response = page.goto('https://www.zhipin.com/', timeout=30000, wait_until='domcontentloaded')
            print(f"Response: {response.status if response else 'None'}")
            
            page.wait_for_timeout(3000)
            
            print(f"Title: {page.title()}")
            page.screenshot(path='/tmp/zhipin_fast.png')
            print("Screenshot saved to /tmp/zhipin_fast.png")
            ctx.close()
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    run()
