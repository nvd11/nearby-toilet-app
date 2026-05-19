#!/bin/bash
COMPARTMENT="ocid1.tenancy.oc1..aaaaaaaa637exp5j4jghtg3lb4x2atqyvl5jllet5cubgsauhsc3mvgm5nga"
OCI="~/.local/bin/oci"

echo "1. Creating VCN (vpc0)..."
VCN_JSON=$(~/.local/bin/oci network vcn create --compartment-id $COMPARTMENT --display-name "vpc0" --cidr-block "10.0.0.0/16" --wait-for-state AVAILABLE)
VCN_ID=$(echo $VCN_JSON | grep -oP '"id": "\K[^"]+' | head -1)
echo "VCN ID: $VCN_ID"

echo "2. Creating Internet Gateway (vpc0-igw)..."
IGW_JSON=$(~/.local/bin/oci network internet-gateway create --compartment-id $COMPARTMENT --vcn-id $VCN_ID --is-enabled true --display-name "vpc0-igw" --wait-for-state AVAILABLE)
IGW_ID=$(echo $IGW_JSON | grep -oP '"id": "\K[^"]+' | head -1)

echo "3. Fetching Default Route Table..."
RT_ID=$(~/.local/bin/oci network vcn get --vcn-id $VCN_ID | grep -oP '"default-route-table-id": "\K[^"]+')

echo "4. Updating Default Route Table to route internet traffic to IGW..."
~/.local/bin/oci network route-table update --rt-id $RT_ID --route-rules "[{\"cidrBlock\":\"0.0.0.0/0\",\"networkEntityId\":\"$IGW_ID\"}]" --force

echo "5. Creating Public Subnet (vpc0-subnet0)..."
SUBNET_JSON=$(~/.local/bin/oci network subnet create --compartment-id $COMPARTMENT --vcn-id $VCN_ID --display-name "vpc0-subnet0" --cidr-block "10.0.0.0/24" --route-table-id $RT_ID --wait-for-state AVAILABLE)
SUBNET_ID=$(echo $SUBNET_JSON | grep -oP '"id": "\K[^"]+' | head -1)
echo "Subnet ID: $SUBNET_ID"

echo "Done!"
