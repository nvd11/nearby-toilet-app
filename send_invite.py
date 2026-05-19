import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

subject = "Draft: Invitation: Tech Sharing - Unlocking LLM Potential with RAG Agent Architecture"

body = """Hi Team,

Following our previous session on ReAct Agents, I’m excited to invite you to our next technical deep-dive! 

While Large Language Models (LLMs) like GPT-4 and Gemini are incredibly smart, they inherently suffer from knowledge blind spots, stale data, and severe hallucinations when dealing with enterprise-specific data. 

How do we securely inject our private knowledge into LLMs? How do we build an architecture that provides precise, traceable, and automated answers? The answer is RAG (Retrieval-Augmented Generation) Agent.

In this upcoming session, we will deconstruct the RAG architecture from the ground up, using real Python code, Object-Oriented Programming (OOP) concepts, and Vector Database strategies.

What we will cover:
* The Limits of LLMs: Why prompt engineering alone isn't enough.
* Deconstructing RAG: The mechanics behind the Retriever and the Generator.
* The Vectorization Magic: How Embedding models cluster semantics and why text search (SQL LIKE) fails us.
* Database & Hybrid Search: Solving the "Recipe vs. Washing Machine" dilemma using Metadata Pre-filtering.
* The Art of Chunking: How to slice data efficiently without losing semantic context.
* Agent Orchestration: A code walkthrough of our RAGAgent using Dependency Injection and "Early Exit" patterns to save API costs.
* The Future of our SDLC: Our vision for vectorizing Jira, Confluence, and Change Requests to revolutionize our daily workflows.

⚠️ Preparation Note: 
As this session involves a fair amount of codebase walkthroughs and architectural concepts (especially Python OOP designs), I highly recommend taking a quick look at the presentation slides beforehand to familiarize yourself with the context. 
👉 [Please insert the link to the Presentation / GitHub Repo here]

Event Details:
* Date: [Please insert Date]
* Time: [Please insert Time]
* Location / Zoom Link: [Please insert Link]
* Presenter: Jason

P.S. We will also tease a critical upcoming topic: How do we scientifically evaluate if our RAG pipeline is actually accurate? Stay tuned for a sneak peek into the automated-rag-evaluator!

Looking forward to seeing you all there and exploring how we can build the next generation of our internal tools together!

Best regards,

Jason
"""

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
