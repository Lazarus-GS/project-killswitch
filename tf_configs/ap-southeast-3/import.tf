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
region     = "ap-southeast-3"
access_key = "CDFYRVWI6RZVLWYPVY0M"
secret_key = "A0U1YivtYl8Rfk8Dea8WwHi2oyiSg0npTEqac8rq"
}
import {
id = "0c921abc-1a5b-44ab-ad8f-cd722da519d0"
to = huaweicloud_networking_secgroup.imported_security-groups2
}
import {
id = "17a879ae-dc7c-4a82-bff3-962daa143db9"
to = huaweicloud_vpc.imported_vpcs2
}
