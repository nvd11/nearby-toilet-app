import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_DEMISE_STRATEGY_PLAN.md"
with open(md_path, "r") as f:
    content = f.read()

# Replace the SFTP Server section in Phase 2
old_sftp = """| **SFTP Server (VM) Provisioning** | RCDP Team | Provision a dedicated SFTP VM (Compute Engine) integrated with Cloud Storage (via GCSFuse). This provides a drop zone for PaaS upstreams unable to mount NAS or call APIs, landing files instantly in the data lake. |"""
new_sftp = """| **Containerized SFTP Ingestion Gateway** | RCDP Team | Provision a cloud-native SFTP endpoint (e.g., deploying an OpenSSH container cluster on GKE fronted by a TCP Network Load Balancer). This containerized approach avoids managing legacy VMs while seamlessly persisting incoming files directly to Cloud Storage via the GCS FUSE CSI driver. |"""

content = content.replace(old_sftp, new_sftp)

with open(md_path, "w") as f:
    f.write(content)

