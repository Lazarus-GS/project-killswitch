terraform {
required_providers {
huaweicloud = {
source  = "huaweicloud/huaweicloud"
version = ">= 1.6.0"
}
}
}

# Configure the HuaweiCloud Provider
provider "huaweicloud" {
region     = "cn-east-3"
access_key = "CDFYRVWI6RZVLWYPVY0M"
secret_key = "A0U1YivtYl8Rfk8Dea8WwHi2oyiSg0npTEqac8rq"
}
import {
id = "69a03701-af0f-41a5-86c6-e609f3304a37"
to = huaweicloud_networking_secgroup.imported_security-groups4
}
