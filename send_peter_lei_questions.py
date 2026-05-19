import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "雷志强 (Peter LEI) - 20道深度真实性验证面试题及参考答案"

body = """Boss,

针对雷志强（Peter LEI）的简历，我为您设计了20道专门用于“打假”和“挤水分”的面试题。

他的简历特点是：英语大专出身、培训班转行，一直在做外包（3段汇丰外包经历），罗列了非常多汇丰内部的项目代号（如 WPB, ICCM, SAPI/PAPI, Enabler Platform）和特定技术（BigQuery, Pebble, RAML, Splunk）。
这20道题将围绕这些“专有名词”和“业务细节”展开。如果他是真的自己做过，一定能说出非常具体的业务痛点和细节；如果是编造或仅是边缘打杂，会在细节追问下原形毕露。

---

### 第一部分：当前项目（TEK 外包到汇丰）- 重点考察 GCP 与 BigQuery 真实性
**1. 关于 BigQuery 的真实连接方式**
*   **题目**：简历提到你实现了从 34 个 Market 获取最新数据的 API，用到了 GCP 和 BigQuery。请问你在 Spring Boot 中是通过什么方式连接 BigQuery 的？是传统的 JDBC 还是 Google Cloud Java Client API？
*   **考察点**：真实性。BigQuery 虽支持 JDBC，但在云原生项目中通常推荐使用官方的 `google-cloud-bigquery` 库。如果他说用 MyBatis/Hibernate 像连 MySQL 一样连 BigQuery，大概率是吹牛。

**2. BigQuery 的查询延迟与计费**
*   **题目**：BigQuery 是 OLAP 数据库，查询延迟通常以秒计。你这个 API 是实时给前端返回 34 个 market 的数据吗？如果是，你是怎么解决 BigQuery 查询慢的问题的？
*   **考察点**：真实性。真实的 GCP 开发者知道 BigQuery 不适合做高频低延迟的实时 API 查询。正确的做法通常是把结果同步到 Redis 或 Cloud SQL（PostgreSQL）中供 API 读取，或者加上缓存。

**3. GCP 标签（Labels）的监控逻辑**
*   **题目**：你提到写了 API 在 GCP 中通过 label name 和 label value 添加标签来监控 API 调用次数。请问这是通过 GCP 的哪个服务来实现的？（比如 Cloud Monitoring / Stackdriver 还是 Logging？）
*   **考察点**：细节。看他是否知道 GCP Cloud Monitoring 的 custom metrics（自定义指标）或者如何在 Log entry 中打 label。

**4. Pebble Template 的使用场景**
*   **题目**：你提到用 Pebble template 自动生成 auth rule。Pebble 是一个比较小众的模板引擎，你们当时为什么选它而不是 FreeMarker 或 Thymeleaf？它的语法和什么最像？
*   **考察点**：细节真实性。Pebble 语法非常像 Python 的 Jinja2 或者是 Twig。如果他支支吾吾，说明这块代码不是他写的。

**5. 配置文件拆分与安全**
*   **题目**：你提到把 auth rule info 和 sql、project id 等主信息从 properties 配置文件中分离开。在汇丰的真实部署环境中，这类敏感的 Project ID 和 Auth 规则最终是存放在哪里的？（比如 HashiCorp Vault 还是 K8s Secrets？）
*   **考察点**：外包员工对汇丰 SRE 部署链路的了解深度。


### 第二部分：上一段汇丰经历（Farben 外包）- 重点考察 WPB Enabler Platform
**6. SAML 与 SAML3 策略**
*   **题目**：简历中写道“Check if all APIs under WPB runs with rational policies of SAML, SAML3”。你能解释一下在你们系统中，SAML 和所谓的 SAML3 策略在实际应用中有什么区别吗？
*   **考察点**：压测名词真实性。业界通用的是 SAML 2.0，其实没啥官方的 SAML 3.0。如果“SAML3”是汇丰内部的某种特定策略代号，他必须能解释清楚这是内部定制的什么规则。如果他开始背诵网上的 SAML 八股文，说明这个工作内容是抄来的。

**7. Buildpack 版本的同步**
*   **题目**：你提到“Synchronized buildpack versions and policies across environments”。在汇丰，你们是用什么云平台或 CI/CD 工具来管理这些 Buildpack 的？（比如 Tanzu/PCF 或 Jenkins）具体怎么同步的？
*   **考察点**：DevOps 真实性。汇丰大量使用 PCF (Pivotal Cloud Foundry) / Tanzu，Buildpack 是 Cloud Foundry 的核心概念。

**8. Splunk 日志查询实操**
*   **题目**：既然你在上个项目用了 Splunk 查 API 信息。如果我现在要查昨天某个特定 API（比如 `/wpb/v1/payment`）的 HTTP 500 错误数量，你能口述一下大致的 SPL (Splunk Search Processing Language) 语句吗？
*   **考察点**：日常使用的真实性。至少应该能说出 `index="..." sourcetype="..." "/wpb/v1/payment" status=500 | stats count` 这类基础语法。

**9. TestNG 与 API 测试重构**
*   **题目**：你负责了升级 API 的 TestNG 测试。在做 API 接口的自动化测试时，你们是如何 mock 上游依赖和 SAML 鉴权过程的？
*   **考察点**：测试深度。看他是否使用 WireMock、Mockito 或者汇丰内部的 Stub 工具。


### 第三部分：GienTech 汇丰项目 - 重点考察 ICCM 与 MuleSoft 生态
**10. RAML 与 SAPI/PAPI 架构**
*   **题目**：你提到理解并开发了 SAPI/PAPI APIs 以及 RAML 规范。这听起来非常像 MuleSoft (API-led connectivity) 的架构（System API, Process API, Experience API）。你们当时是用 Java (Spring Boot) 实现的，还是用 MuleSoft 实现的？RAML 文件在你们开发流程中的作用是什么？
*   **考察点**：架构名词真实性。RAML 是 RESTful API Modeling Language，MuleSoft 的标配。看他是真的遵循 API 优先（Design-first）通过 RAML 生成代码骨架，还是乱写的词。

**11. 批处理与实时流的隔离**
*   **题目**：你处理了 email 和 SMS 的 time-critical, realtime, 和 batch 任务。这三种类型的通知，在底层的消息队列或线程池设计上，是如何做到隔离，保证 batch（批量发信）不会阻塞 realtime（实时验证码）的？
*   **考察点**：架构经验水分。真实的应对方案必须是分为不同的 Kafka Topic，或者使用不同优先级的队列，分配不同数量的消费者实例。

**12. XSL 邮件模板的 Java 渲染**
*   **题目**：你提到处理 XSL email templates。在 Java 代码里，你们通常用什么原生的类库或者第三方库将 XML 数据与 XSL 模板转换成最终的 HTML 邮件的？
*   **考察点**：API 细节。真实做过的应该会提到 `javax.xml.transform.Transformer`，`TransformerFactory`。


### 第四部分：过往经历与前端框架真伪 (Hydsoft / Beyondsoft)
**13. SAP HANA 数据库差异**
*   **题目**：在 Hydsoft 期间你用了 Spring Boot 和 HANA 数据库。通过 MyBatis 连 HANA 和连 MySQL，在配置或者写 SQL 时遇到过什么明显的方言差异吗？
*   **考察点**：真实经历核实。

**14. React 框架真伪测试**
*   **题目**：你的简历“Technical Skills”里赫然写着“Good mastery of React framework”。请问在 React 函数组件中，`useEffect` 和 `useMemo` 有什么核心区别？如果依赖数组传空数组 `[]` 代表什么？
*   **考察点**：挤水分。很多后端随便改改前端页面就敢写“精通/良好掌握”。传空数组代表只在组件挂载时执行一次。

**15. Weblogic 部署差异**
*   **题目**：2019 年在平安集团你用了 Weblogic。一个标准的 Spring Boot 应用如果要打成 war 包扔进 Weblogic 跑，相比于自带 Tomcat 跑 jar 包，在代码配置上需要做哪两步核心修改？
*   **考察点**：老技术的踩坑经验。必须排除内嵌 Tomcat 依赖，并且启动类要继承 `SpringBootServletInitializer` 并重写 `configure` 方法。


### 第五部分：核心技术栈与架构能力（压测深度）
**16. Spring 框架源码级理解**
*   **题目**：你用了7年 SSM 和 Spring Boot。请问 Spring 解决 Bean 循环依赖的核心机制是什么？为什么需要三级缓存而不是两级？
*   **考察点**：培训班常见八股文，看看他的基础是否扎实。

**17. Kafka 的防重复消费**
*   **题目**：简历上写了 Kafka。如果发短信的 batch 任务向 Kafka 投递了 10 万条消息，消费者在消费过程中宕机重启，如何保证同一条短信绝对不会被发送两次（避免客诉）？
*   **考察点**：幂等性设计的真实经验。依靠 DB 的唯一索引或 Redis 记录消息处理状态。

**18. K8s 的基础排障**
*   **题目**：你写了“a good grasp of Docker and Kubernetes”。假设你在汇丰 UAT 环境发现一个 Pod 状态是 `CrashLoopBackOff`，你一般会使用哪两条 `kubectl` 命令去排查原因？
*   **考察点**：日常操作真实性。预期答案：`kubectl describe pod <pod-name>` (看事件) 和 `kubectl logs <pod-name> --previous` (看上一次崩溃的日志)。

**19. SQL 注入防范**
*   **题目**：在 MyBatis 中，`${}` 和 `#{}` 有什么区别？如果我想在 SQL 里做个动态的 `ORDER BY` 字段名，应该用哪一个？怎么防注入？
*   **考察点**：基础安全常识。`ORDER BY` 字段名必须用 `${}`（因为 `#{}` 会加引号导致语法错误），但必须在 Java 代码层做好白名单过滤防注入。

**20. 个人真实成长与极限**
*   **题目**：你是英语专业转行做 Java，做了7年外包。抛开业务 CRUD，在这 7 年里，你个人亲自排查过最复杂的线上技术问题（比如 OOM 内存溢出、死锁、或者 CPU 100%）是什么？请具体讲讲你是怎么定位并解决的。
*   **考察点**：摸底。没有任何外包能把一段“编造”的深度排障经历讲得天衣无缝。如果没有，说明他始终处于打杂写业务接口的层级。

---
邮件已送达，这20题就像个筛子，是李逵还是李鬼，一试便知！
"""

msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully")
except Exception as e:
    print(f"Failed to send email: {e}")
    sys.exit(1)
