# AWS Moon Proxy Manager

## Description
This skill manages the Boss's AWS resources, specifically the "Moon proxy" VM located in the Singapore region, using the AWS CLI.

## Credentials & Environment
* **AWS_ACCESS_KEY_ID**: `AKIASWTV5OGNY6BNSZH2`
* **AWS_SECRET_ACCESS_KEY**: `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`
* **IAM User**: `moon-cli`
* **AWS CLI Path**: `/home/gateman/.local/bin/aws`

## Target Instance Details
* **Instance ID**: `i-0a1fd6da467e3d020`
* **Region**: `ap-southeast-1` (Singapore)
* **Instance Type**: `t3.micro`
* **Known Public IP**: `13.212.67.185`

## Common Commands

### 1. Check Instance Status
```bash
env AWS_ACCESS_KEY_ID=AKIASWTV5OGNY6BNSZH2 AWS_SECRET_ACCESS_KEY="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" /home/gateman/.local/bin/aws ec2 describe-instances --region ap-southeast-1 --instance-ids i-0a1fd6da467e3d020 --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress]' --output table
```

### 2. Ping Test
```bash
ping -c 4 13.212.67.185
```

### 3. Start/Stop Instance
```bash
# Start
env AWS_ACCESS_KEY_ID=AKIASWTV5OGNY6BNSZH2 AWS_SECRET_ACCESS_KEY="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" /home/gateman/.local/bin/aws ec2 start-instances --region ap-southeast-1 --instance-ids i-0a1fd6da467e3d020

# Stop
env AWS_ACCESS_KEY_ID=AKIASWTV5OGNY6BNSZH2 AWS_SECRET_ACCESS_KEY="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" /home/gateman/.local/bin/aws ec2 stop-instances --region ap-southeast-1 --instance-ids i-0a1fd6da467e3d020
```

## Note
Always use the full path to `aws` (`/home/gateman/.local/bin/aws`) and pass the credentials inline via `env` to avoid configuring global state that might conflict with other GCP/AWS setups.