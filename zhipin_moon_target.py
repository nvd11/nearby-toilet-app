from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        try:
            print("Launching Chromium on Moon...")
            ctx = p.chromium.launch_persistent_context(
                user_data_dir='/home/gateman/.config/chromium',
                headless=False,
                executable_path='/usr/bin/chromium',
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--remote-debugging-port=9222'
                ]
            )
            page = ctx.pages[0] if len(ctx.pages) > 0 else ctx.new_page()
            
            print("Navigating to Zhipin...")
            response = page.goto('https://www.zhipin.com/', timeout=60000)
            print(f"Response: {response.status if response else 'None'}")
            
            page.wait_for_timeout(5000)
            
            print(f"Title: {page.title()}")
            print(f"URL: {page.url}")
            
            page.screenshot(path='/tmp/zhipin_moon.png')
            print("Screenshot saved.")
            time.sleep(5)
            ctx.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    run()
