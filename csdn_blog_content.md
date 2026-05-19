# 放弃 Selenium 吧，Playwright 才是现代 Web 自动化测试与爬虫的终极杀器

说实话，搞 Web 自动化和写爬虫这么多年，以前一直是用 Selenium，简直是一把鼻涕一把泪。每次 Chrome 更新，还得去找对应版本的 `chromedriver`，而且脚本里总是充斥着各种 `time.sleep()` 和显式等待。要是不加等待，分分钟给你报个 `Element is not clickable at point`，玄学报错让人怀疑人生。

直到最近项目组里有人安利了微软开源的 **Playwright**，试用了一周之后，我只能说两个字：真香！这篇博客就当做是我的入门笔记，把环境搭建和一个最基础但也最实用的例子分享给大家，希望能帮到还没入坑的朋友。

## 为什么推荐 Playwright？

相比老牌的 Selenium，Playwright 解决了几个痛点：

1. **环境配置零痛苦**：不用你去下载什么 driver 配置环境变量，一行命令它连浏览器本体都能给你下载好。
2. **自动等待机制（Auto-waiting）**：这绝对是杀手锏。你让它点击一个按钮，它会自动等待这个按钮出现在 DOM树里、变成可见状态、并且停止动画可以被点击。再也不用写那种死循环去轮询元素了！
3. **多浏览器内核原生支持**：Chromium、Firefox、WebKit（Safari），它都支持，而且接口统一。
4. **无缝支持网络拦截**：你可以轻松修改 Request 或者拦截 Response，这对爬虫来说简直是神器。

## 极简安装指南

前提是你已经安装好了 Python 3.7 或以上版本。打开终端，依次执行下面两行命令：

```bash
# 1. 安装 Python 的 Playwright 库
pip install playwright

# 2. 安装 Playwright 运行所需的浏览器（Chromium, Firefox, WebKit）
playwright install
```
*注：如果你只打算用 Chromium（通常爬虫足够了），可以运行 `playwright install chromium` 节省一点下载时间。*

## 第一个实战例子：打开网页并自动截图

废话不多说，我们直接上代码。这个例子的功能是：打开浏览器，访问百度，获取网页的标题，然后把整个页面截个图保存下来。

新建一个文件叫 `demo.py`，粘贴以下代码：

```python
from playwright.sync_api import sync_playwright

def main():
    # 1. 启动 Playwright 上下文管理器
    with sync_playwright() as p:
        # 2. 启动 Chromium 浏览器，headless=False 代表我们要看到浏览器界面
        browser = p.chromium.launch(headless=False, slow_mo=50)
        
        # 3. 创建一个新的浏览器上下文（相当于打开一个无痕模式的全新窗口，缓存独立）
        context = browser.new_context()
        
        # 4. 在上下文中打开一个新的标签页
        page = context.new_page()
        
        # 5. 导航到目标网址
        print("正在访问百度...")
        page.goto('https://www.baidu.com/')
        
        # 6. 获取页面的 Title
        title = page.title()
        print(f"当前网页标题是: {title}")
        
        # 7. 在搜索框输入文本并点击搜索
        # Playwright 支持多种定位方式，这里直接用 id 定位
        page.locator('#kw').fill('Playwright Python')
        page.locator('#su').click()
        
        # 8. 等待搜索结果加载出来（等待某个元素出现）
        page.wait_for_selector('#content_left')
        
        # 9. 截图保存
        page.screenshot(path='search_result.png')
        print("截图已保存为 search_result.png")
        
        # 10. 关闭浏览器
        browser.close()

if __name__ == '__main__':
    main()
```

### 代码逐行详解

考虑到有些刚接触的朋友，我把每一部分拆开详细解释一下：

- `with sync_playwright() as p:` ：Playwright 提供了同步（Sync）和异步（Async）两套 API。对于绝大多数脚本和爬虫任务，同步 API 就足够用了。`with` 语句会自动帮我们在代码执行完毕后清理底层的资源。
- `p.chromium.launch(headless=False, slow_mo=50)`：这是启动浏览器的核心。`headless=False` 意思是**非无头模式**，你可以亲眼看着浏览器弹出来自动点点点，非常适合开发调试！`slow_mo=50` 意思是把每个操作（比如打字、点击）延迟 50 毫秒，不然它跑得太快肉眼根本看不清。
- `browser.new_context()` 和 `context.new_page()`：Playwright 引入了 Context 的概念。一个 Browser 可以有多个 Context，每个 Context 的 Cookie、LocalStorage 都是完全隔离的。这就意味着你可以同时模拟两个不同用户的登录状态，互相不串号。
- `page.locator(...).fill(...)`：`locator` 是 Playwright 强推的元素定位方式。它不像 Selenium 一开始就去查找元素，而是在真正执行动作（如 `fill` 填入文字，`click` 点击）的那一刻才去查找，并配合自动等待机制，稳得不行。
- `page.wait_for_selector(...)`：虽然有自动等待，但有些操作（比如点击完搜索之后）我们需要确认页面确确实实加载出了新内容再进行下一步（比如截图）。这行代码会一直挂起，直到指定的元素出现在页面上。

## 总结

上面只是 Playwright 的冰山一角，如果你亲自跑一下这段代码，一定会惊讶于它的运行速度和稳定性。

后续如果有时间，我再写写进阶的用法，比如如何利用它自带的录制脚本功能（Codegen）点点鼠标就能生成代码，或者如何注入 Cookie 绕过登录拦截。

大家如果有遇到什么坑，或者有什么爬虫方向的问题，欢迎在评论区留言交流！我们下期见~
