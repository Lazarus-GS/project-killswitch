# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "6ff70391-0712-4cc9-b77b-669076bcb021"
resource "huaweicloud_networking_secgroup" "imported_security-groups3" {
  delete_default_rules  = null
  description           = "Allowing traffic on all ports may introduce security risks. Exercise caution when selecting this option."
  enterprise_project_id = "cc8e405d-638b-4e5b-a81f-e945bf626e66"
  name                  = "sg-all"
  region                = "cn-south-1"
  timeouts {
    delete = null
  }
}

# __generated__ by Terraform from "ea8ad119-3d85-4612-97e8-8d89bcec7a73"
resource "huaweicloud_vpc" "imported_vpcs4" {
  cidr                  = "172.16.0.0/12"
  description           = null
  enterprise_project_id = "cc8e405d-638b-4e5b-a81f-e945bf626e66"
  name                  = "vpc-001"
  region                = "cn-south-1"
  secondary_cidr        = null
  tags                  = {}
  timeouts {
    create = null
    delete = null
  }
}

# __generated__ by Terraform from "16b79b85-2cbc-42bc-a121-005f82cf93d2"
resource "huaweicloud_vpc" "imported_vpcs3" {
  cidr                  = "192.168.0.0/16"
  description           = null
  enterprise_project_id = "cc8e405d-638b-4e5b-a81f-e945bf626e66"
  name                  = "vpc-002"
  region                = "cn-south-1"
  secondary_cidr        = null
  tags                  = {}
  timeouts {
    create = null
    delete = null
  }
}
