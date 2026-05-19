from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        try:
            print("Launching Chrome directly via Playwright...")
            ctx = p.chromium.launch_persistent_context(
                user_data_dir='/home/gateman/.config/google-chrome-stealth',
                headless=False,
                executable_path='/opt/google/chrome/chrome',
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--remote-debugging-port=9222'
                ]
            )
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            
            print("Navigating to Zhipin...")
            response = page.goto('https://www.zhipin.com/', timeout=60000)
            print(f"Response: {response.status if response else 'None'}")
            page.wait_for_timeout(5000)
            
            print(f"Title: {page.title()}")
            print(f"Content length: {len(page.content())}")
            
            page.screenshot(path='/tmp/zhipin_moon_method.png')
            print("Screenshot saved.")
            
            # Keep it running a bit so Boss can see
            import time
            time.sleep(10)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    run()
