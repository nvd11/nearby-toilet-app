#!/bin/bash
# OCI ARM Poller - High Availability Version
# Managed by systemd

# Environmental setup
export PATH="/home/gateman/.local/bin:/usr/local/bin:/usr/bin:/bin"
OCI="/home/gateman/.local/bin/oci"
COMPARTMENT="ocid1.tenancy.oc1..aaaaaaaa637exp5j4jghtg3lb4x2atqyvl5jllet5cubgsauhsc3mvgm5nga"
AD="NqKU:AP-SINGAPORE-1-AD-1"
SUBNET="ocid1.subnet.oc1.ap-singapore-1.aaaaaaaagkwgt3egr6tegmpc4lrptqsxoa4kmukwftr3d2kl2ooiqtlvuoua"
IMAGE="ocid1.image.oc1.ap-singapore-1.aaaaaaaa2noeixre53oja5vuhpr6gddojbfsirefd3gfrpz4bryrkiobo6jq"
PUB_KEY="/home/gateman/.openclaw/workspace/ssh-key.pub"
LOG_FILE="/home/gateman/.openclaw/workspace/poll_arm.log"

echo "[$(date)] --- ARM Poller HA Service Boot ---" >> "$LOG_FILE"

# Prevent multiple instances
PIDFILE="/tmp/poll_arm.pid"
if [ -f "$PIDFILE" ]; then
  PID=$(cat "$PIDFILE")
  if ps -p "$PID" > /dev/null 2>&1; then
    echo "[$(date)] Instance already running (PID: $PID). Exiting." >> "$LOG_FILE"
    exit 1
  fi
fi
echo $$ > "$PIDFILE"

while true; do
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  
  # Launch attempt with 180s timeout to prevent hanging (Oracle API is slow)
  OUTPUT=$(timeout 180 "$OCI" compute instance launch \
    --compartment-id "$COMPARTMENT" \
    --availability-domain "$AD" \
    --shape "VM.Standard.A1.Flex" \
    --shape-config '{"ocpus": 4, "memoryInGBs": 24}' \
    --subnet-id "$SUBNET" \
    --image-id "$IMAGE" \
    --assign-public-ip true \
    --display-name "free-arm-vm" \
    --ssh-authorized-keys-file "$PUB_KEY" 2>&1)
  
  EXIT_CODE=$?

  if [ $EXIT_CODE -eq 124 ]; then
    echo "[$TIMESTAMP] Status: OCI CLI Timed out. Retrying in 30s..." >> "$LOG_FILE"
    sleep 30
    continue
  fi

  if echo "$OUTPUT" | grep -qE "Out of capacity|Out of host capacity"; then
    WAIT_TIME=600 # 10 minutes
    echo "[$TIMESTAMP] Status: Out of capacity. Next try in ${WAIT_TIME}s." >> "$LOG_FILE"
    sleep $WAIT_TIME
  elif echo "$OUTPUT" | grep -q "TooManyRequests"; then
    echo "[$TIMESTAMP] Status: Rate limited. Backing off 1 hour." >> "$LOG_FILE"
    sleep 3600
  elif echo "$OUTPUT" | grep -q '"lifecycle-state": "PROVISIONING"'; then
    echo "[$TIMESTAMP] SUCCESS! ARM INSTANCE CREATED!" >> "$LOG_FILE"
    echo "$OUTPUT" >> "$LOG_FILE"
    echo "$OUTPUT" > /home/gateman/.openclaw/workspace/success_launch.log
    exit 0
  else
    echo "[$TIMESTAMP] Status: Unexpected Error/Timeout. Logging and retrying in 60s." >> "$LOG_FILE"
    echo "$OUTPUT" | head -n 10 >> "$LOG_FILE"
    sleep 60
  fi
done
