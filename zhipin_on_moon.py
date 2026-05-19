from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        print("Launching Chromium on Moon...")
        ctx = p.chromium.launch_persistent_context(
            user_data_dir='/home/gateman/.config/chromium-stealth',
            headless=False,
            executable_path='/usr/bin/chromium',
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--disable-infobars',
                '--hide-crash-restore-bubble'
            ]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        
        print("Navigating to Zhipin...")
        try:
            response = page.goto('https://www.zhipin.com/', timeout=60000)
            print(f"Response: {response.status if response else 'None'}")
        except Exception as e:
            print(f"Goto error: {e}")
            
        page.wait_for_timeout(5000)
        print(f"Title: {page.title()}")
        print(f"URL: {page.url}")
        
        page.screenshot(path='/tmp/zhipin_moon_final.png')
        print("Screenshot saved to /tmp/zhipin_moon_final.png")
        ctx.close()

if __name__ == '__main__':
    run()
