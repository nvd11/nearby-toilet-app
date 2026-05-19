import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_DEMISE_STRATEGY_PLAN.md"
with open(md_path, "r") as f:
    content = f.read()

# Replace the GKE/Containerized SFTP section back to GCE
old_gke = """| **Containerized SFTP Ingestion Gateway** | RCDP Team | Provision a cloud-native SFTP endpoint (e.g., deploying an OpenSSH container cluster on GKE fronted by a TCP Network Load Balancer). This containerized approach avoids managing legacy VMs while seamlessly persisting incoming files directly to Cloud Storage via the GCS FUSE CSI driver. |"""
new_gce = """| **SFTP Server (GCE VM) Provisioning** | RCDP Team | Provision a dedicated SFTP landing zone using Google Compute Engine (GCE) integrated with Cloud Storage (via GCSFuse). This provides a secure, traditional drop zone for upstream systems unable to mount NAS or call APIs, allowing files to land seamlessly in the data lake. |"""

content = content.replace(old_gke, new_gce)

with open(md_path, "w") as f:
    f.write(content)

