---
name: oci-manager
description: Manage Oracle Cloud Infrastructure (OCI) using the oci-cli. Use this skill when asked to create instances, list compute resources, manage VCNs, or perform automated tasks like polling for free-tier ARM instances in Oracle Cloud.
---

# Oracle Cloud Infrastructure (OCI) Manager

This skill leverages the `oci-cli` to manage the user's Oracle Cloud environment, specifically targeting their `ap-singapore-1` region with the `alice-sa` service account.

## Prerequisites & Environment

- **CLI Tool:** `oci` is installed at `~/.local/bin/oci`. Use this absolute path when executing commands.
- **Config file:** `~/.oci/config`
- **Private Key:** `/home/gateman/.openclaw/workspace/alice-sa.pem`
- **Tenancy/Compartment OCID:** `ocid1.tenancy.oc1..aaaaaaaa637exp5j4jghtg3lb4x2atqyvl5jllet5cubgsauhsc3mvgm5nga`

## Creating an Instance (e.g. Free Tier ARM)

When creating a compute instance, you often need to provide:
- `--compartment-id`: Always use the tenancy OCID provided above.
- `--availability-domain`: Retrieve using `~/.local/bin/oci iam availability-domain list`.
- `--shape`: For the free-tier ARM instance, use `VM.Standard.A1.Flex`.
- `--shape-config`: For max free-tier ARM, set `{"ocpus": 4, "memoryInGBs": 24}`.
- `--subnet-id`: Ensure a VCN and subnet exist, or list them using `~/.local/bin/oci network subnet list --compartment-id ...`.
- `--image-id`: Find an Oracle Linux or Ubuntu ARM image OCID via `~/.local/bin/oci compute image list ... --shape VM.Standard.A1.Flex`.

*Note on Capacity:* Creating instances in `ap-singapore-1` often fails with an "Out of host capacity" (HTTP 500) error. You should wrap creation commands in a bash script or Python loop if the user requests automated polling.

## Examples

### 1. Listing Availability Domains
```bash
~/.local/bin/oci iam availability-domain list
```

### 2. Listing Instances
```bash
~/.local/bin/oci compute instance list --compartment-id ocid1.tenancy.oc1..aaaaaaaa637exp5j4jghtg3lb4x2atqyvl5jllet5cubgsauhsc3mvgm5nga
```

### 3. Listing VCNs
```bash
~/.local/bin/oci network vcn list --compartment-id ocid1.tenancy.oc1..aaaaaaaa637exp5j4jghtg3lb4x2atqyvl5jllet5cubgsauhsc3mvgm5nga
```

## Troubleshooting
- If you see `NotAuthorizedOrNotFound`, it may mean the `alice-sa` API user lacks permissions for a specific resource, or you need to add specific permissions in the Oracle Cloud Console under Policies. (The current user has `manage instance-family` and `manage virtual-network-family`).
