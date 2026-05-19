#!/bin/bash
OCI="/home/gateman/.local/bin/oci"
COMPARTMENT="ocid1.tenancy.oc1..aaaaaaaa637exp5j4jghtg3lb4x2atqyvl5jllet5cubgsauhsc3mvgm5nga"
AD="NqKU:AP-SINGAPORE-1-AD-1"
SUBNET="ocid1.subnet.oc1.ap-singapore-1.aaaaaaaagkwgt3egr6tegmpc4lrptqsxoa4kmukwftr3d2kl2ooiqtlvuoua"
IMAGE="ocid1.image.oc1.ap-singapore-1.aaaaaaaal6x46iqzk3dfhvin3oay37ljct62yvby6blyqhlrocgm6gmmsspq"
PUB_KEY="/home/gateman/.openclaw/workspace/ssh-key.pub"
LOG_FILE="/home/gateman/.openclaw/workspace/try_amd.log"

TIMESTAMP=$(date)
echo "[$TIMESTAMP] Attempting to launch AMD instance..." >> "$LOG_FILE"

OUTPUT=$($OCI compute instance launch \
  --compartment-id "$COMPARTMENT" \
  --availability-domain "$AD" \
  --shape "VM.Standard.E2.1.Micro" \
  --subnet-id "$SUBNET" \
  --image-id "$IMAGE" \
  --assign-public-ip true \
  --display-name "free-amd-vm" \
  --ssh-authorized-keys-file "$PUB_KEY" 2>&1)

if echo "$OUTPUT" | grep -qE "Out of capacity|Out of host capacity"; then
  echo "[$TIMESTAMP] Result: Out of capacity." >> "$LOG_FILE"
elif echo "$OUTPUT" | grep -q '"lifecycle-state": "PROVISIONING"'; then
  echo "[$TIMESTAMP] SUCCESS! AMD Instance is provisioning!" >> "$LOG_FILE"
  echo "$OUTPUT" >> "$LOG_FILE"
  echo "AMD VM CREATED" > /home/gateman/.openclaw/workspace/amd_success.log
else
  echo "[$TIMESTAMP] Result: Unknown response or error." >> "$LOG_FILE"
  echo "$OUTPUT" >> "$LOG_FILE"
fi
