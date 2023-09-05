# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "69a03701-af0f-41a5-86c6-e609f3304a37"
resource "huaweicloud_networking_secgroup" "imported_security-groups4" {
  delete_default_rules  = null
  description           = "The security group is for general-purpose web servers and includes default rules that allow all inbound ICMP traffic and inbound traffic on ports 22, 80, 443, and 3389. The security group is used for remote login, ping, and hosting a website on ECSs."
  enterprise_project_id = "cc8e405d-638b-4e5b-a81f-e945bf626e66"
  name                  = "sg-46ab"
  region                = "cn-east-3"
  timeouts {
    delete = null
  }
}
