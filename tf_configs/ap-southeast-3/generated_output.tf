# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "0c921abc-1a5b-44ab-ad8f-cd722da519d0"
resource "huaweicloud_networking_secgroup" "imported_security-groups2" {
  delete_default_rules  = null
  description           = "Allowing traffic on all ports may introduce security risks. Exercise caution when selecting this option."
  enterprise_project_id = "cc8e405d-638b-4e5b-a81f-e945bf626e66"
  name                  = "sg-Geethaka"
  region                = "ap-southeast-3"
  timeouts {
    delete = null
  }
}

# __generated__ by Terraform from "17a879ae-dc7c-4a82-bff3-962daa143db9"
resource "huaweicloud_vpc" "imported_vpcs2" {
  cidr                  = "192.168.0.0/16"
  description           = null
  enterprise_project_id = "cc8e405d-638b-4e5b-a81f-e945bf626e66"
  name                  = "vpc-GS"
  region                = "ap-southeast-3"
  secondary_cidr        = null
  tags                  = {}
  timeouts {
    create = null
    delete = null
  }
}
