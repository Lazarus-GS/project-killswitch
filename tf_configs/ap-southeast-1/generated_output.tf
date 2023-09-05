# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "75c95a41-7491-4ded-ba34-c1bbc5ce89f6"
resource "huaweicloud_networking_secgroup" "imported_security-groups1" {
  delete_default_rules  = null
  description           = "The security group is for general-purpose web servers and includes default rules that allow all inbound ICMP traffic and inbound traffic on ports 22, 80, 443, and 3389. The security group is used for remote login, ping, and hosting a website on ECSs."
  enterprise_project_id = "cc8e405d-638b-4e5b-a81f-e945bf626e66"
  name                  = "sg-Geethaka-HK"
  region                = "ap-southeast-1"
  timeouts {
    delete = null
  }
}

# __generated__ by Terraform from "58a5997f-aa17-4b83-9030-a8e5643ccd35"
resource "huaweicloud_vpc" "imported_vpcs1" {
  cidr                  = "192.168.0.0/16"
  description           = null
  enterprise_project_id = "cc8e405d-638b-4e5b-a81f-e945bf626e66"
  name                  = "vpc-Geethaka"
  region                = "ap-southeast-1"
  secondary_cidr        = null
  tags                  = {}
  timeouts {
    create = null
    delete = null
  }
}
