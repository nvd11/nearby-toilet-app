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
msg['Subject'] = "徐燕鹏 - 第三波面试题：微服务架构、分布式系统与TL故障排查"

body = """Boss,

这是为您准备的第三波面试题（共10题）。这批题目重点挖掘徐燕鹏简历中提到的 **Spring Cloud 生态组件、分布式架构设计（分布式事务/锁/消息）、CI/CD（Jenkins/Docker）以及他作为 Tech Lead 的线上排障能力**。这套题非常适合用来“压测”他16年经验的水分。

---

### 1. Spring Cloud 旧组件的升级替换（结合简历：Eureka/Zuul/Ribbon/Hystrix）
**题目：** 你在简历的技能列表中提到了 Eureka、Zuul、Ribbon 和 Hystrix。但这些 Netflix OSS 组件目前基本都已停止维护。如果我们要用较新的 Spring Cloud 版本来重构汇丰的 MI 系统，你会使用哪些现代组件来替换它们？为什么？
**参考答案与考察点：**
- **考察点：** 架构视野和技术迭代跟进能力。
- **答案：** 
  - Zuul -> **Spring Cloud Gateway** (基于 WebFlux 非阻塞，性能远超 Zuul 1.x)。
  - Hystrix -> **Resilience4j** 或 **Alibaba Sentinel**。
  - Ribbon -> **Spring Cloud LoadBalancer** (官方推荐替代品)。
  - Eureka -> **Consul**, **Nacos** 或直接依赖 **K8s native Service Discovery**。

### 2. 阻塞调用与非阻塞客户端（结合简历：Feign 与 Reactor-core）
**题目：** 简历提到你熟悉 Feign，同时目前在汇丰项目里又用了 `reactor-core` 进行并行 API 调用。OpenFeign 默认是阻塞式的，如果在 WebFlux/Reactor 的环境下直接使用传统 Feign 会有什么隐患？你会如何解决？
**参考答案与考察点：**
- **考察点：** 响应式编程与微服务调用的结合陷阱。
- **答案：** 隐患：在 Event Loop 线程中执行传统 Feign 的同步 HTTP 请求会阻塞底层的 Netty 线程，导致整个服务吞吐量断崖式下跌，甚至直接卡死。
- **解决方案：** 应该使用 `WebClient` 进行纯异步非阻塞调用，或者引入第三方开源的 `ReactiveFeign`。

### 3. 微服务分布式事务（结合简历：PostgreSQL, MongoDB, Spring Cloud）
**题目：** 在你目前的汇丰项目中，技术栈同时包含 PostgreSQL 和 MongoDB。假设有一个业务：服务 A 将一条流水记录写入 PostgreSQL 后，通过 REST API 或 Kafka 调用服务 B，服务 B 需要在 MongoDB 中更新该用户的报表状态。如果服务 B 宕机或处理失败，你如何保证两个数据库的数据最终一致性？
**参考答案与考察点：**
- **考察点：** 分布式事务实战（避免纸上谈兵的 2PC）。
- **答案：** 微服务下不推荐强一致性事务（如 XA/Seata AT），推荐**最终一致性**方案。
  - **方案A（可靠消息/Outbox Pattern）：** 服务A在写 PostgreSQL 时，同事务写入一张本地消息表（Outbox）。然后由定时任务或 Debezium 监听 Binlog，把消息可靠地发到 Kafka。服务 B 消费并保证幂等。
  - **方案B（Saga Pattern）：** 采用补偿机制，若服务B失败，则调用服务A的补偿接口回滚流水状态。

### 4. 关系型与文档型数据库选型（结合简历：当前项目同时使用 PG 和 Mongo）
**题目：** 既然你的当前项目同时用到了 PostgreSQL 和 MongoDB。对于管理信息（MI）系统，PostgreSQL 也有强大的 JSONB 数据类型支持。你能说说为什么一定要引入 MongoDB 吗？在什么具体的业务场景下，PG 的 JSONB 无法替代 MongoDB？
**参考答案与考察点：**
- **考察点：** 数据库选型深度。
- **答案：** PG JSONB 适合结构偶尔变化但不作为重度查询条件的场景。但如果需要对嵌套极深的 JSON 文档进行极其复杂的聚合分析（Aggregation Pipeline），或者面临单表 TB 级别的海量写入且需要开箱即用的分片（Sharding）横向扩展能力，MongoDB 更加成熟和纯粹。

### 5. Redis 分布式锁的深水区（结合简历：高并发安全、Redis）
**题目：** 你提到处理高并发安全。很多系统用 Redis 的 `SETNX` 做分布式锁，但这存在几个经典问题：比如业务执行时间超过了锁的过期时间导致锁被提前释放；又比如线程 A 解了线程 B 的锁。如果你是 Tech Lead，你会如何规范团队对分布式锁的使用？
**参考答案与考察点：**
- **考察点：** 分布式锁的边缘 case 处理。
- **答案：** 
  - 避免手写裸的 `SETNX`。
  - 规范团队直接使用 **Redisson** 客户端。
  - 解释原理：Redisson 内置了 **Watchdog（看门狗）**机制，后台线程会自动为未执行完的业务进行锁续期；且释放锁时采用 Lua 脚本，先校验当前锁的 value（如 UUID+ThreadId）是否属于自己，再进行删除，保证解铃还须系铃人的原子性。

### 6. Kafka 零丢失与Exactly-Once（结合简历：Kafka、容错）
**题目：** 如果 MI 系统通过 Kafka 接收核心交易系统的流水数据，一条都不能丢，同时也绝不能重复计算。在 Kafka 的 Producer 端和 Consumer 端，你分别需要做哪些核心配置和代码设计来实现 Exactly-Once（精确一次）的语义？
**参考答案与考察点：**
- **考察点：** 消息队列高可靠性配置。
- **答案：** 
  - **Producer：** 配置 `acks=all`，开启幂等性（`enable.idempotence=true`），配置重试次数（`retries`），并确保 Topic 的 `min.insync.replicas` >= 2。
  - **Consumer：** 关闭自动提交（`enable.auto.commit=false`），采用手动提交 Offset。为防止重复消费，消费者的业务逻辑**必须自己做幂等设计**（如利用流水号在 DB 做唯一索引），因为 Kafka 无法阻止网络重发导致的重复。

### 7. Jenkins Pipeline 与 Docker 结合（结合简历：Jenkins pipeline部署, Docker）
**题目：** 你在简历中写了使用 Jenkins pipeline 进行部署。你能口述一下，一个标准的微服务从 Git 提交代码到最终打包成 Docker 镜像并部署到 K8s/云服务器，它的 `Jenkinsfile` 大致包含哪几个核心的 Stage（阶段）？
**参考答案与考察点：**
- **考察点：** DevOps 真实动手能力，是否真的写过 Pipeline。
- **答案：** 标准的 Declarative Pipeline 阶段：
  1. **Checkout:** 拉取 Git 代码。
  2. **Build/Test:** 执行 `mvn clean package` 并且跑单元测试。
  3. **Code Quality:** SonarQube 代码扫描（可选）。
  4. **Docker Build:** 执行 `docker build -t xxx:v1 .`。
  5. **Docker Push:** 登录私有镜像仓（Harbor/ACR）并推送镜像。
  6. **Deploy:** 使用 `kubectl apply` 或 Helm 升级 K8s 部署。

### 8. API 安全与认证鉴权（结合汇丰银行业务背景）
**题目：** 在银行环境下，对外或对内的 RESTful API 安全要求极高。如果我们要对外暴露一个 MI 数据查询 API，仅仅使用 HTTPS 足够吗？通常你会结合哪些技术来保证 API 的防篡改、防重放、以及认证授权？
**参考答案与考察点：**
- **考察点：** 银行业务安全意识。
- **答案：** HTTPS 只解决传输加密。还需要：
  - **认证授权：** 采用 OAuth 2.0 / OIDC (JWT Token) 或汇丰内部的 SAML 协议校验用户身份。
  - **防篡改：** 请求体加签（Signature），客户端用私钥加密 hash，服务端用公钥验签。
  - **防重放：** 使用 Timestamp + Nonce（随机数），服务端使用 Redis 记录短时间内的 Nonce，拒绝过期或重复的请求。

### 9. 核心校验逻辑的架构设计（结合简历：写过平台核心库校验逻辑）
**题目：** 简历提到你在平台核心库中编写了“System verification logic”。如果系统的校验规则经常随着业务线的要求而频繁变化（比如各种复杂的 if-else 条件），每次修改代码都要重新发布，作为 Tech Lead 你会引入什么设计模式或组件来优化它？
**参考答案与考察点：**
- **考察点：** 代码架构设计、开闭原则（OCP）。
- **答案：** 
  - **设计模式层：** 使用 **策略模式 (Strategy)** 结合 **责任链模式 (Chain of Responsibility)**，将每种校验规则解耦为独立的 Handler，通过 Spring 动态注入 List。
  - **组件库层：** 引入规则引擎（如 **Drools**, **LiteFlow** 或使用 Spring Expression Language **SpEL**），把规则配置化并存入数据库，实现热更新。

### 10. 线上 OOM 故障排查实战（结合简历：16年经验 / TL）
**题目：** 作为技术负责人，如果某天线上 K8s 里的 MI 系统某个 Pod 频繁报 `java.lang.OutOfMemoryError: Java heap space` 并被探针重启，影响了报表导出。你会采取怎样的一套标准排查流程来定位内存泄漏的代码？
**参考答案与考察点：**
- **考察点：** 资深 Java 工程师必备的 JVM 线上排障能力。
- **答案：** 
  1. **保留现场：** 启动参数必须配置 `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/log/`，让应用在 OOM 时自动生成 Dump 文件，并通过持久卷（PV）保存。
  2. **日志监控：** 查看 Grafana/Prometheus 监控 JVM 堆内存趋势。
  3. **离线分析：** 将 Dump 文件下载到本地，使用 **MAT (Memory Analyzer Tool)** 或 VisualVM 分析。
  4. **定位大对象：** 在 MAT 中查看 `Dominator Tree` 或 `Histogram`，找到占用内存最多的类（如往往是由于一次性从 DB 查询了几十万条记录没有分页，或者是 `ThreadLocal` 未调用 `remove()` 导致的内存泄漏）。

---
这10题问完，绝对能把他的技术底细摸得一清二楚！祝您顺利！
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
