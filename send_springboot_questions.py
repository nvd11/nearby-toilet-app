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
msg['Subject'] = "徐燕鹏 - 10道基于简历的 Spring Boot 深度面试题及参考答案"

body = """Boss,

这是为您准备的第二波面试题，专门针对徐燕鹏简历中重度使用的 **Spring Boot**，并结合他简历中提到的其他技术栈（Reactor-core, K8s, MongoDB, 自研平台组件, 云平台部署等）进行了深度定制。这些题目适合用来评估他作为技术负责人的底层技术深度。

---

### 1. Spring Boot 自动装配原理（结合简历：资深开发 / TL经验）
**题目：** 你使用了多年的 Spring Boot，请简述 `@SpringBootApplication` 注解的底层工作原理。Spring Boot 是如何知道要加载哪些第三方库的配置的？在 Spring Boot 2.7 或 3.x 中，自动装配的加载机制有什么重要变化？
**参考答案与考察点：**
- **考察点：** 基础底层原理。
- **答案：** `@SpringBootApplication` 是一个复合注解，核心是 `@EnableAutoConfiguration`。它通过 `SpringFactoriesLoader` 扫描 classpath 下所有的 `META-INF/spring.factories` 文件（在旧版本中），或者 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 文件（Spring Boot 2.7+ 引入的新机制），加载所有配置好的 AutoConfiguration 类。条件注解（如 `@ConditionalOnClass`, `@ConditionalOnMissingBean`）决定了哪些 Bean 最终会被注册到 IoC 容器中。

### 2. Spring Boot 自定义 Starter 设计（结合简历：2025.03“写过平台工具组件如敏感字符过滤”）
**题目：** 简历提到你写过“敏感字符过滤、时间组件”等平台工具。如果我们要把这个“敏感词过滤”功能做成一个企业内部通用的 Spring Boot Starter，供其他微服务直接引入使用，你需要做哪些步骤？
**参考答案与考察点：**
- **考察点：** TL级别的组件化思维和实战能力。
- **答案：** 
  1. 创建独立的 Maven/Gradle 工程。
  2. 编写核心功能类（如 `SensitiveWordFilterService`）和配置属性类（`@ConfigurationProperties`，用于在 `application.yml` 中自定义黑名单路径等）。
  3. 编写自动配置类（使用 `@Configuration`, `@ConditionalOnProperty` 开关控制是否启用自动配置，并注册核心 Bean）。
  4. 将自动配置类的全限定名配置到 `META-INF/spring.factories` 或 `AutoConfiguration.imports` 文件中。
  5. 打包发布到私有 Maven 仓库（Nexus）。

### 3. Spring Boot 与响应式编程（结合简历：当前汇丰项目使用 reactor-core）
**题目：** 简历提到你在当前汇丰的 API 开发中使用了 `reactor-core`。在 Spring Boot 环境下，引入 Spring WebFlux 后，底层的内嵌 Web 容器会发生什么变化？传统的过滤器（Filter）和拦截器（Interceptor）在 WebFlux 中如何等价实现？
**参考答案与考察点：**
- **考察点：** 对响应式技术栈在 Spring Boot 中的集成的理解。
- **答案：** 默认内嵌容器会从 Tomcat 切换为基于事件驱动的 Netty（Reactor Netty）。传统的 `javax.servlet.Filter` 和 `HandlerInterceptor` 将无法使用，需要替换为 WebFlux 提供的 `WebFilter`，或者使用基于路由函数的拦截功能，以非阻塞（Non-blocking）的方式处理请求。

### 4. 外部化配置与云平台优先级（结合简历：部署在亚马逊云、阿里云、Spring Cloud Config）
**题目：** 在公有云（AWS/阿里云）或 K8s 环境中部署 Spring Boot 应用时，我们需要在不同的环境（Dev/UAT/Prod）使用不同的数据库密码和云服务的 Secret。Spring Boot 支持多种配置来源，如果 `application.yml`、环境变量（Environment Variables）、命令行参数（Command Line Args）和 Spring Cloud Config Server 存在同名的属性，它们的加载优先级是怎样的？
**参考答案与考察点：**
- **考察点：** 运维部署与配置管理能力。
- **答案：** 优先级从高到低依次为：命令行参数 > 系统环境变量 > Spring Cloud Config Server (通常注入为高优先级的 PropertySource) > application-{profile}.yml > application.yml。在云原生最佳实践中，密码和 Secret 通常通过 K8s Secrets 注入为系统环境变量，以覆盖打包在 jar 内的 yml 配置。

### 5. Spring Boot Actuator 与 Kubernetes 探针结合（结合简历：K8S经验）
**题目：** 结合你在 K8S 上的经验，Spring Boot 的 Actuator 如何与 K8S 的 Liveness（存活）和 Readiness（就绪）探针完美配合？在什么场景下，Readiness 会变成 DOWN 状态但 Liveness 依然是 UP 状态？
**参考答案与考察点：**
- **考察点：** 云原生运维与高可用机制。
- **答案：** Spring Boot 2.3+ Actuator 自动提供了 Kubernetes 探针支持（`/actuator/health/liveness` 和 `/actuator/health/readiness`）。
- **状态区别：** 如果应用正在进行大量数据处理或外部依赖（如数据库/外部API）暂时断开，应用可以自己把 Readiness 设置为 DOWN，告诉 K8S 停止把外部流量路由给这个 Pod，但此时进程没有死锁，Liveness 依然是 UP 的（所以 K8s 不会杀掉重启这个 Pod）。等外部依赖恢复，Readiness 自动切回 UP 继续接客。

### 6. Spring Boot 优雅停机 Graceful Shutdown（结合简历：高可用架构与 Jenkins 部署）
**题目：** MI 系统有大量的耗时 API 请求。当我们在 Jenkins 流水线触发部署或在 K8S 中更新镜像时，直接杀进程会导致用户请求中断。在 Spring Boot 中如何配置真正的优雅停机（Graceful Shutdown）？它的内部逻辑是怎样的？
**参考答案与考察点：**
- **考察点：** 生产环境的工程化思维。
- **答案：** 在 `application.yml` 中配置 `server.shutdown=graceful`，并配置超时时间 `spring.lifecycle.timeout-per-shutdown-phase`。
- **内部逻辑：** 当收到 SIGTERM 信号时，内嵌 Web 容器（如 Tomcat/Netty）停止接受新的网络连接（拒绝新请求），但会让已接受且正在处理中的请求继续执行，直到完成或达到配置的超时时间，最后才彻底销毁 Spring IoC 容器。

### 7. 高并发下的内嵌容器调优（结合简历：支持高并发安全性）
**题目：** Spring Boot 默认使用内嵌的 Tomcat 容器。假设我们的 MI 后端遇到了高并发的 QPS 峰值，大量请求开始排队。你可以通过 `application.yml` 中的哪些核心参数对内嵌的 Tomcat 进行调优？
**参考答案与考察点：**
- **考察点：** JVM 与容器的性能调优经验。
- **答案：** 候选人应能说出类似以下参数：
  - `server.tomcat.threads.max`（最大工作线程数，默认200，高并发下适当调大）。
  - `server.tomcat.threads.min-spare`（核心/最小空闲线程数）。
  - `server.tomcat.accept-count`（全连接队列/操作系统排队长度，默认100，超过的请求直接被 Refuse 掉）。
  - `server.tomcat.max-connections`（Tomcat 能同时处理的最大连接数，NIO 默认10000）。

### 8. Spring Boot 数据访问与 MongoDB 连接池（结合简历：深度使用 MongoDB）
**题目：** 简历中多次提到使用 MongoDB。在 Spring Boot 中使用 `spring-boot-starter-data-mongodb` 时，底层默认的连接池是如何管理的？如果网络经常出现波动导致连接泄漏，你会在配置中添加哪些超时或保活参数？
**参考答案与考察点：**
- **考察点：** 数据库驱动层面的踩坑经验。
- **答案：** 默认使用 MongoDB Java Driver 自带的连接池。可以通过 `spring.data.mongodb.uri` 配置选项（如 `maxPoolSize` 限制最大连接），并需要配置心跳保活和超时策略，例如 `connectTimeoutMS`（连接超时），`socketTimeoutMS`（Socket 读取超时），以及 `maxIdleTimeMS`（防止被防火墙悄悄杀死的死连接）。

### 9. AOP 与自定义注解实现接口幂等性（结合简历：RESTful 幂等性）
**题目：** 简历中写道“Experienced at RESTful API design... supports idempotency”。如果要在 Spring Boot 中实现一个通用的、对业务代码无侵入的幂等性校验，你会如何使用 Spring AOP 和自定义注解来完成？如何处理高并发下的竞争条件？
**参考答案与考察点：**
- **考察点：** Spring AOP 实战能力。
- **答案：** 
  1. 定义一个 `@Idempotent` 注解。
  2. 编写切面类 `@Aspect`，使用 `@Around` 拦截带有该注解的方法。
  3. 在切面逻辑中，从请求头（Header）中提取幂等 Token 或 Request ID。
  4. 利用 Redis 的 `setIfAbsent`（SETNX）指令，将 Token 作为 Key 存入 Redis，并设置 TTL（如10分钟）。
  5. 如果 SETNX 成功，执行 `joinPoint.proceed()`；如果失败，说明是重复请求，直接抛出 `IdempotentException` 或返回友好提示（或者返回上一次缓存的结果）。

### 10. 全局异常处理机制（结合简历：API 容错与系统校验）
**题目：** 在开发 MI 系统的 API 时，如果系统出现各种预期的业务异常和未捕获的系统异常，如何在 Spring Boot 中实现一个统一的、标准化的 REST 响应结构来包裹这些错误？
**参考答案与考察点：**
- **考察点：** 规范化后端工程的开发能力。
- **答案：** 使用 `@ControllerAdvice`（或 `@RestControllerAdvice`）加上 `@ExceptionHandler` 注解。
  - 定义一个统一的 `Result<T>` 响应类或 `ErrorResponse` 格式（包含 code, message, data, traceId）。
  - 根据不同的 Exception 类（如 `MethodArgumentNotValidException` 处理参数校验错误，`BusinessException` 处理业务逻辑错误，`Exception` 兜底处理未知错误）分别编写拦截方法，并封装成统一的 JSON 格式返回。

---
建议在面试时挑几道他最相关的题目深入探讨。邮件发送完毕，祝您面试顺利！
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
