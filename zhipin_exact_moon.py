from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        try:
            print("Launching exactly like Moon...")
            ctx = p.chromium.launch_persistent_context(
                user_data_dir='/home/gateman/.config/google-chrome',
                headless=False,
                args=['--remote-debugging-port=9222'],
                executable_path='/usr/bin/google-chrome-stable'
            )
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            
            print("Navigating to Zhipin...")
            response = page.goto('https://www.zhipin.com/web/user/?ka=header-login', timeout=60000)
            page.wait_for_timeout(5000)
            
            print(f"Title: {page.title()}")
            print(f"Content length: {len(page.content())}")
            
            page.screenshot(path='/tmp/zhipin_exact_moon.png')
            print("Screenshot saved.")
            
            ctx.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    run()
