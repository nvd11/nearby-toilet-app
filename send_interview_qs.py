import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_emails = ["jason1.pan@hsbc.com.hk", "gateman56@gmail.com"]

body = """Boss,

这是为您准备的候选人 张华 (Hoy Zhang) 的 20 道验真面试题库（重点考察履历真实性及实战经验）：

一、 针对最近一段经历 (GCP & Workload Identity) - 必考！
1. Workload Identity 实操： 你在把 GCP GSA 映射给 K8s Pod 时，具体是怎么配置 KSA 和 GSA 绑定的？（测谎点：必须提到 iam.workloadIdentityUser 角色绑定和在 KSA 上打 annotation。）
2. 权限排障： 如果 Pod 里的应用报错说没有权限访问 GCP 资源（比如 Storage 或 BigQuery），你怎么排查是 KSA 没绑对、GSA 本身缺 IAM 角色，还是应用代码没走 Default Azure/Google Credentials？
3. Terraform 状态管理： 你们用 Terraform 做 CD 时，tfstate 文件存在哪里？多个人或者多个 Pipeline 并发跑的时候，怎么解决 state lock 冲突的问题？
4. 认证安全： 你的 Jenkins/GitLab CI 调用 gcloud 或 Terraform 跑 GCP 部署时，凭证是怎么注入的？（测谎点：如果说直接把 Service Account JSON key 存在明文里是大忌，应提到 Secret Manager、Vault 或 Workload Identity Federation。）

二、 Kubernetes 核心深水区 (验证 Ericsson/Advent 经验)
5. GitOps 冲突： 你们用 ArgoCD。如果生产环境中，有人紧急通过 kubectl edit 手动改了一个 Deployment 的副本数，ArgoCD 会发生什么？你们团队是怎么处理这种配置漂移 (Configuration Drift) 的？
6. Helm 踩坑： 用 Helm upgrade 更新应用时，如果 pre-upgrade hook 执行失败了，这个 release 会变成什么状态？你是怎么处理并回滚的？
7. K8s 疑难杂症： 描述一次你处理过的最难搞的 Pod 处于 CrashLoopBackOff 的经历。你具体用了哪些命令和思路定位到最终原因的？
8. 探针机制： Readiness Probe 和 Liveness Probe 最大的区别是什么？如果 Liveness 配置得过于敏感，会造成什么生产灾难？
9. 监控实战： Prometheus 和 Grafana 配置中，你写过哪些比较复杂的 PromQL 告警规则？比如怎么监控并告警“某个 Pod 在过去 10 分钟内频繁重启”？

三、 CI/CD 与自动化流水线 (验证 Jenkins/Groovy)
10. Shared Library： 描述一个你自己亲手写的、被多条 Pipeline 复用的 Groovy Method。在写 Jenkins 脚本时遇到过 Script Security Sandbox 拦截报错吗？怎么解决的？
11. 灾备经验： Jenkins Master 节点如果突然宕机，你们的恢复流程是什么？Job 的配置和构建历史怎么保全？
12. 多环境发布： 比较一下你用过的 Jenkins 和 GitLab CI，在做一套代码打一个镜像，流转 Dev -> UAT -> Prod 时，环境变量和差异化配置在 Pipeline 里怎么管理最优雅？
13. 自动化测试卡点： CI 流水线里如果集成 SonarQube 代码扫描，你们是怎么做到“扫描不达标就直接阻断 Merge”的？

四、 Terraform 进阶 (验证 IaC 真实能力)
14. Tainted State： 运行 terraform apply 过程中如果网络断了或者中途失败，导致某个资源建了一半，Terraform 会怎么标记它？下次 apply 会怎样？怎么修复？
15. 危险操作规避： 遇到过 terraform plan 显示要 destroy and recreate 某个核心资源（比如 RDS 数据库），但你其实只是想改一个非破坏性属性的情况吗？你是怎么绕过或处理的？（测谎点：应提到 lifecycle { prevent_destroy = true } 或 terraform state rm、moved 等高级命令。）
16. 模块化： 你们的 Terraform 是全写在一个 main.tf 里，还是用了 Modules？不同环境的 variables 怎么拆分管理的？

五、 Linux 排障与网络基础 (为我们的 Proxy/NAT 需求摸底)
17. 系统高负载排障： 生产服务器突然收到告警 Load Average 极高，但 CPU 只有 20%，你登上去后的前 3 个排查命令是什么？（测谎点：看是否知道 top 看 iowait，vmstat，strace 抓 I/O 阻塞等。）
18. SNAT 机制： 既然我们 JD 强调网络。虽然你没怎么搞过 Cloud NAT，但在传统的 K8s 或 Linux 里，内网机器要上公网拉取包，流量出去时 IP 是怎么转换的 (SNAT)？
19. 代理环境： 如果在一台完全没有公网 IP 的内网 Linux 机器上，你需要通过公司的 HTTP Proxy 才能拉取 Docker 镜像，你需要配置哪个具体的文件或环境变量？（测谎点：Docker daemon.json 的 proxies 配置，或者 HTTP_PROXY 变量注入。）
20. 脚本安全： 你用 Python/Shell 写运维自动化脚本时，脚本如果需要连数据库，账号密码你怎么处理，以确保不会泄露或打在日志里？

祝面试顺利！
-- Alice
"""

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ", ".join(receiver_emails)
msg['Subject'] = "GCP DevOps 候选人 (张华) 验真面试题库"
msg.attach(MIMEText(body, 'plain', 'utf-8'))

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_emails, msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
