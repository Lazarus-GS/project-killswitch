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
region     = "cn-south-1"
access_key = "CDFYRVWI6RZVLWYPVY0M"
secret_key = "A0U1YivtYl8Rfk8Dea8WwHi2oyiSg0npTEqac8rq"
}
import {
id = "6ff70391-0712-4cc9-b77b-669076bcb021"
to = huaweicloud_networking_secgroup.imported_security-groups3
}
import {
id = "16b79b85-2cbc-42bc-a121-005f82cf93d2"
to = huaweicloud_vpc.imported_vpcs3
}
import {
id = "ea8ad119-3d85-4612-97e8-8d89bcec7a73"
to = huaweicloud_vpc.imported_vpcs4
}
