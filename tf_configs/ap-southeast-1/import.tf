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
region     = "ap-southeast-1"
access_key = "CDFYRVWI6RZVLWYPVY0M"
secret_key = "A0U1YivtYl8Rfk8Dea8WwHi2oyiSg0npTEqac8rq"
}
import {
id = "75c95a41-7491-4ded-ba34-c1bbc5ce89f6"
to = huaweicloud_networking_secgroup.imported_security-groups1
}
import {
id = "58a5997f-aa17-4b83-9030-a8e5643ccd35"
to = huaweicloud_vpc.imported_vpcs1
}
