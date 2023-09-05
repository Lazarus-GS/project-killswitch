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
region     = "cn-north-1"
access_key = "CDFYRVWI6RZVLWYPVY0M"
secret_key = "A0U1YivtYl8Rfk8Dea8WwHi2oyiSg0npTEqac8rq"
}
import {
id = "34b81993-ed65-43b8-8a02-4cafd416b4a3"
to = huaweicloud_vpc.imported_vpcs5
}
