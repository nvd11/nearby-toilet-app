from playwright.sync_api import sync_playwright

text_to_fill = """17年金融科技与合规数据平台研发与架构经验，现任顶级外资银行（汇丰）技术研发经理（ITSO）。深耕 GCP 云原生架构与大型数据工程（Data Engineering），同时具备丰富的 AI Agent 企业级应用落地经验。擅长将复杂业务需求转化为高可用架构，寻求数据架构工程师或 AI/数据结合领域的挑战性机会。

🎯 核心竞争力：
1. 大规模云数据架构与工程 (GCP Data Engineering)：
精通 GCP 数据生态体系 (BigQuery, Dataflow/Apache Beam, Cloud Storage, Pub/Sub)。目前正主导部门核心数据平台 (RCDP) 的云原生重构与“去 Oracle 化”大盘，成功规划并实施传统 ETL (Informatica) 向 Dataflow 的现代化迁移方案，精通批流一体化处理及实时数据管道接入方案。
2. 企业级 AI Agent 研发与 MLOps 实践：
具备将大模型 (LLM) 能力融入企业级业务全栈的实战经验。熟练使用 LangChain 框架，主导开发风控合规 RAG Agent (Project ADA)，并独立设计了基于 Golden Dataset 的模型响应自动化评估机制（语义相似度+事实性）。负责数据科学家团队 ML 模型 (PyTorch) 的工程化部署与 MLOps 生产级全链路监控。
3. 研发效能优化 (DevOps) 与智能工具链：
熟练掌握敏捷开发管理及自动化流水线建设 (Jenkins, Ansible)。热衷于自研提效工具，曾开发打通 GitHub Webhook 与 Gemini LLM 的自动化 Code Review 机器人（引入 Human-in-the-loop 机制持续优化 Prompt），以及对接 Jira/Confluence 的 Agent 应用，极大提升团队工程效能。
4. 微服务演进与复合型业务底蕴：
扎实的 Java/Python/Spring Cloud 微服务开发功底。深谙金融合规与风控业务逻辑及外企安全标准，能完美平衡技术创新与严苛的企业级数据安全合规要求。"""

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9224")
    context = browser.contexts[0]
    page = context.new_page()
    
    print("Navigating to Boss Zhipin Resume page in a new tab...")
    try:
        page.goto("https://www.zhipin.com/web/geek/resume", timeout=15000)
    except Exception as e:
        print("Goto exception (usually fine):", e)
        
    page.wait_for_timeout(3000)
    print("Current URL:", page.url)
    
    if "login" in page.url:
        print("Redirected to login. The cookies might not be present or Boss needs to login again.")
        page.screenshot(path="/home/gateman/.openclaw/workspace/boss_state.png")
    else:
        # We are on the resume page (or jobs page)
        if "resume" not in page.url:
            print("Not on resume page, trying to click resume tab...")
            try:
                page.locator("text=简历").first.click(timeout=3000)
                page.wait_for_timeout(3000)
            except Exception:
                pass
                
        print("Looking for Edit button for 个人优势...")
        js_code = """() => {
            let els = Array.from(document.querySelectorAll('*')).filter(el => el.innerText && el.innerText.trim() === '个人优势');
            if(els.length === 0) return 'no 个人优势 element';
            
            let target = els[els.length - 1]; // usually the innermost
            let container = target.closest('.resume-item, .item-primary') || target.parentElement.parentElement;
            if(!container) return 'no container';
            
            let editBtns = Array.from(container.querySelectorAll('.op-edit, .icon-edit, a, button, span')).filter(el => el.innerText === '编辑' || el.className.includes('edit'));
            let editBtn = editBtns[0];
            if(editBtn) {
                editBtn.click();
                return 'clicked';
            }
            return 'edit button not found in container';
        }"""
        res = page.evaluate(js_code)
        print("JS click result:", res)
        
        page.wait_for_timeout(2000)
        
        # Check if textarea appeared
        textarea = page.locator("textarea").first
        if textarea.is_visible():
            print("Filling text...")
            textarea.fill(text_to_fill)
            page.wait_for_timeout(1000)
            
            print("Clicking Save...")
            save_btn = page.locator("button:has-text('保存'), button:has-text('完成'), a:has-text('保存')").first
            if save_btn.is_visible():
                save_btn.click()
                print("Saved successfully!")
            else:
                print("Save button not found.")
        else:
            print("Textarea not found after clicking edit.")
            
        page.screenshot(path="/home/gateman/.openclaw/workspace/boss_state.png")
        print("Automation finished.")
