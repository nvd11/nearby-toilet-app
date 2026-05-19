import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "徐燕鹏 - 汇丰 GCP MI System Java 后端面试题及参考答案"

body = """Boss,

根据您提供的徐燕鹏简历，结合“汇丰 GCP cloudbase MI SYSTEM java backend”岗位要求，我针对他简历中提及的Java、Spring Cloud、微服务、K8s、数据库、响应式编程等技术点，为您精心准备了10道深度面试题及参考答案。这些题目旨在刺探他16年经验的真实技术深度，而非背诵八股文。

---

### 1. Java多线程与并发控制 (结合简历：对多线程有深入理解)
**题目：** 在实现 MI 系统（管理信息系统）的数据聚合时，如果我们需要并行调用5个下游系统的 API 来组装一份报表（如你近期在汇丰项目里提到的并行处理），你会如何设计和配置线程池？如果其中一个下游系统突然响应极慢，如何避免主业务线程池资源被全部耗尽？
**参考答案与考察点：**
- **配置：** 考察是否提及自定义 `ThreadPoolExecutor`，根据 IO 密集型特性设置合理的线程数（如 2N 或更高），以及设置合适的阻塞队列和拒绝策略。
- **防耗尽：** 考察隔离机制（Bulkhead pattern）。优秀候选人应提到为不同下游系统分配独立线程池，或使用 `CompletableFuture` 设置超时时间（`orTimeout()`），或使用熔断器（如 Resilience4j）在超时频发时直接切断，防止级联雪崩。

### 2. 响应式编程与阻塞调用 (结合简历：目前在汇丰使用了 reactor-core)
**题目：** 简历中提到在汇丰现项目使用了 `reactor-core` 进行 API 开发。相比传统 Spring MVC，Spring WebFlux 在底层的线程模型有什么不同？在使用 Reactor 开发时，如果不可避免地需要进行一次阻塞式的 JDBC 数据库查询，应该如何处理以防止阻塞 Event Loop？
**参考答案与考察点：**
- **模型对比：** 传统是 Thread-per-request（Tomcat线程池），WebFlux 是基于 Event Loop（Netty），用极少量的线程处理大量并发连接。
- **阻塞处理：** 考察是否真实写过响应式代码。必须提到**绝对不能在 Event Loop 线程中执行阻塞调用**。正确做法是使用 `subscribeOn(Schedulers.boundedElastic())` 将阻塞操作调度到专用的弹性线程池中执行。

### 3. 分布式接口幂等性 (结合简历：RESTful API 设计，支持高并发安全、幂等性)
**题目：** 在分布式环境中（尤其是 MI 报表系统可能存在网络重试），接口幂等性非常重要。请结合你之前的项目，详细讲讲你是如何实现高并发场景下的接口强一致性幂等的？
**参考答案与考察点：**
- **考察真实性：** 避开空泛概念。候选人应提到具体的方案，如：基于 Redis 的分布式锁（SETNX + 过期时间），配合 Token 机制（防重放）；或者利用数据库唯一索引（Unique Key）做兜底拦截去重。结合业务流水号（Transaction ID）做状态机校验。

### 4. 数据库索引原理与优化 (结合简历：MySQL/PostgreSQL, storage indexing principles)
**题目：** 在生成 MI 报表时，经常会遇到多条件组合查询。假设在一张千万级的 MySQL 交易表中，有一个查询条件是 `WHERE status = 1 AND amount > 1000 ORDER BY create_time DESC LIMIT 10`。你会如何为这个查询建立联合索引？为什么？
**参考答案与考察点：**
- **索引原则：** 考察最左前缀原则和 B+ 树特性。
- **正确建立：** 应该建立 `(status, create_time)` 的联合索引。
- **原因解析：** 因为 `status` 是等值查询，放在最左边；`amount` 是范围查询，如果放到中间会导致后面的索引失效；而把 `create_time` 放在 `status` 后面，可以利用索引天然的有序性避免 filesort（文件排序），从而极大地提升 `ORDER BY ... LIMIT` 的性能。

### 5. MongoDB vs 关系型数据库 (结合简历：近期多个项目重度使用 MongoDB)
**题目：** 你的最近几个项目（包括汇丰）都使用了 MongoDB。在处理汇丰的这类数据流转/管理信息系统时，什么场景下你会坚决选择 MongoDB 而不是 PostgreSQL？如果 MongoDB 的数据量达到数亿级别需要 Sharding（分片），你会倾向于基于 Hash 分片还是 Range 分片？
**参考答案与考察点：**
- **选型场景：** 考察对 NoSQL 的理解。当数据结构不固定（Schema-free）、有大量嵌套文档（JSON格式的外部API响应存储），或者需要极高的写入吞吐量且不强依赖复杂事务时，选 MongoDB。
- **分片策略：** Range 分片适合范围查询（如时间段查询报表），但容易导致数据热点（新数据都写在同一个分片）；Hash 分片能保证数据均匀分布，写性能好，但不支持高效的范围查询。需结合实际业务权衡。

### 6. 消息队列的顺序消费 (结合简历：Kafka/ActiveMQ, 架构优化)
**题目：** MI 系统通过 Kafka 接入上游系统的变更事件。如果我们需要保证同一个客户（Customer ID）的所有状态变更消息被严格按照产生顺序处理，你会如何设计 Kafka 的 Producer 和 Consumer？
**参考答案与考察点：**
- **Producer端：** 发送消息时必须指定 Message Key（如使用 Customer ID），Kafka 会根据 Key 的 hash 值将同一客户的消息发送到同一个 Partition。
- **Consumer端：** Kafka 只能保证 Partition 内部有序。消费者单线程消费该 Partition 即可保证顺序；如果在 Consumer 内部还要用多线程处理提速，则必须在内存中再对 Customer ID 进行哈希，分配到对应的内存队列和专属线程中。

### 7. Kubernetes与平滑发布 (结合简历：K8S 经验)
**题目：** 在 Kubernetes (K8S) 环境下部署 Spring Boot 微服务时，如何配置才能实现真正的“零宕机平滑发布”（Zero Downtime Deployment）？请解释 Readiness Probe (就绪探针) 和 Liveness Probe (存活探针) 的作用和区别。
**参考答案与考察点：**
- **平滑发布：** 必须提到配置优雅停机（Spring Boot 的 `server.shutdown=graceful`），并在 K8s 中配合 `preStop` hook 让应用有时间处理完剩余请求。
- **探针区别：** Liveness 探测应用是否死锁或崩溃，失败则重启 Pod；Readiness 探测应用是否准备好接收流量，失败则将 Pod 从 Service 的 Endpoints 中摘除（不重启）。

### 8. 云平台技术映射 (结合简历：AWS、阿里云，申请 GCP 岗位)
**题目：** 你在简历中提到了在 AWS 和阿里云上的部署经验。我们汇丰的这个 MI 项目是基于 Google Cloud Platform (GCP) 的。既然云平台概念相通，你能快速做个映射吗？比如你在 AWS 用的 S3、RDS、EKS、SQS/Kinesis，对应在 GCP 里大概是什么服务？
**参考答案与考察点：**
- 考察对云原生的宏观认知和学习迁移能力。
- **参考映射：** S3 -> GCS (Google Cloud Storage)；RDS -> Cloud SQL；EKS -> GKE (Google Kubernetes Engine)；SQS/Kinesis -> Pub/Sub。

### 9. 高并发下的缓存设计 (结合简历：Redis, 分布式缓存支持高并发)
**题目：** 在高并发报表查询中，如果某个极其耗时的全局统计报表缓存刚好过期，瞬间有大量请求涌入导致数据库压力剧增（缓存击穿），你会如何解决？
**参考答案与考察点：**
- 考察真实的缓存架构经验，而非基础命令。
- **解决方案：**
  1. **互斥锁（Mutex Lock / Redisson）：** 缓存失效时，只有一个线程能拿到锁去查数据库并重建缓存，其他线程等待。
  2. **逻辑过期（永不过期）：** 物理上不设置过期时间，在 Value 内部封存一个逻辑过期时间。一旦发现逻辑过期，异步线程池去更新数据，当前请求直接返回旧数据。

### 10. 微服务容错与降级 (结合简历：Hystrix, fault tolerance)
**题目：** 你在简历中提到了微服务组件 Hystrix。熔断器（Circuit Breaker）的状态机是如何流转的（Closed, Open, Half-Open）？由于 Hystrix 已经停更，如果我们要对 MI 系统进行技术栈升级，你会推荐使用什么组件？它的底层熔断机制有什么演进？
**参考答案与考察点：**
- **状态流转：** 闭合（正常） -> 错误率超阈值 -> 打开（熔断，直接拒绝） -> 过一段时间 -> 半开（放行少量请求试探） -> 成功则闭合，失败则继续打开。
- **升级替代：** 推荐 **Resilience4j** 或 **Sentinel**。
- **区别/演进：** Hystrix 主要基于线程池隔离（开销大，上下文切换重），而 Resilience4j 基于 Java 8 函数式编程设计，非常轻量级，默认使用基于信号量（Semaphore）的隔离机制，不再强绑定线程池。

---

希望这份题库能帮您在面试时准确探测他的真实水平！
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
