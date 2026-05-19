import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Job Description: Senior GCP DevOps Engineer"

body = """Hi Boss,

Here is the GCP DevOps Engineer Job Description as requested:

Job Title: Senior GCP DevOps Engineer

About the Role:
We are seeking a highly skilled and proactive GCP DevOps Engineer to join our engineering team. In this role, you will be responsible for designing, implementing, and maintaining our cloud infrastructure on Google Cloud Platform (GCP). You will play a critical role in ensuring our network architecture is secure, scalable, and highly available, while driving automation across our deployment pipelines. 

Key Responsibilities:
• Cloud Infrastructure Management: Design, deploy, and manage scalable cloud infrastructure utilizing a wide range of GCP products and services.
• Advanced Networking: Architect and maintain complex GCP VPC networks, ensuring secure and efficient routing, firewall configurations, and subnets.
• VM Configuration & Security: Expertly configure, manage, and troubleshoot specialized virtual machines, specifically Proxy VMs and NAT VMs, to manage secure ingress and egress traffic.
• Infrastructure as Code (IaC): Write, review, and maintain robust infrastructure code using Terraform to automate the provisioning of GCP resources.
• CI/CD Automation: Build, optimize, and maintain Continuous Integration and Continuous Deployment (CI/CD) pipelines to enable smooth and rapid software delivery.
• Monitoring & Optimization: Implement proactive monitoring, alerting, and logging solutions to ensure system health and optimize cloud resource costs.

Required Qualifications:
• Proven experience working as a DevOps Engineer, Cloud Engineer, or similar role with a heavy focus on Google Cloud Platform (GCP).
• Deep understanding of GCP networking concepts (VPC, Cloud NAT, Cloud Router, Firewalls, Cloud Load Balancing).
• Hands-on expertise in configuring and managing Proxy VMs and NAT VMs within enterprise environments.
• Strong proficiency in Infrastructure as Code (IaC) tools, primarily Terraform.
• Extensive experience building and managing CI/CD pipelines (e.g., Jenkins, GitLab CI, GitHub Actions, or GCP Cloud Build).
• Strong scripting skills (Python, Bash, or Go) for automation tasks.
• Excellent problem-solving skills and the ability to troubleshoot complex network and infrastructure issues independently.

Preferred Qualifications:
• Google Cloud Professional Cloud Architect or Professional Cloud DevOps Engineer certification.
• Experience with containerization and orchestration (Docker, GKE/Kubernetes).

Best regards,
Alice 💋
"""

msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Success")
except Exception as e:
    print(f"Failed: {e}")
