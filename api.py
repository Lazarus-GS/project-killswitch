import requests
import json
import os
import subprocess


auth_url = "https://eps.myhuaweicloud.com/v3/auth/tokens"
query_url = "https://eps.myhuaweicloud.com/v1.0/enterprise-projects/8ccfc768-35f9-4830-a687-9a258216f376/resources/filter"

auth_headers = {
    "Content-Type": "application/json"
}

auth_json_body = {
 "auth": {
    "identity": {
        "methods": [
            "password"
            ],
            "password": {
                "user": {
                    "name": "Geethaka",
                    "password": "R@nd0m@98",
                    "domain": {
                     "name": "APClouddemoMM"
                    }
                }
            }
        },
        "scope": {
            "domain": {
                "name": "APClouddemoMM"
            }
        }
    }
}

auth_response = requests.post(auth_url, json=auth_json_body, headers=auth_headers)

x_subject_token = auth_response.headers.get('X-Subject-Token')

query_headers = {
    "Content-Type": "application/json",
    "X-Auth-Token": x_subject_token
    #"X-Auth-Token": "MIITVwYJKoZIhvcNAQcCoIITSDCCE0QCAQExDTALBglghkgBZQMEAgEwghFpBgkqhkiG9w0BBwGgghFaBIIRVnsidG9rZW4iOnsiZXhwaXJlc19hdCI6IjIwMjMtMDgtMzBUMDc6MzI6MDkuMTEyMDAwWiIsIm1ldGhvZHMiOlsicGFzc3dvcmQiXSwiY2F0YWxvZyI6W10sImRvbWFpbiI6eyJ4ZG9tYWluX3R5cGUiOiJIV0NfSEsiLCJuYW1lIjoiQVBDbG91ZGRlbW9NTSIsImlkIjoiMDU2MDNkMGJiNTgwMTBmNzBmMjhjMDExNTA2ZDU4YTAiLCJ4ZG9tYWluX2lkIjoiNDQ1MjUzZjU0YTA4NDcxZGIwN2UyYmUxNDE5YTk3YWMifSwicm9sZXMiOlt7Im5hbWUiOiJyZWFkb25seSIsImlkIjoiMCJ9LHsibmFtZSI6InNlcnZlcl9hZG0iLCJpZCI6IjAifSx7Im5hbWUiOiJsdHNfYWRtIiwiaWQiOiIwIn0seyJuYW1lIjoiZnNzX2FkbSIsImlkIjoiMCJ9LHsibmFtZSI6InNmc19hZG0iLCJpZCI6IjAifSx7Im5hbWUiOiJhcGlnX2FkbSIsImlkIjoiMCJ9LHsibmFtZSI6ImRuc19hZG0iLCJpZCI6IjAifSx7Im5hbWUiOiJ2cGNfbmV0YWRtIiwiaWQiOiIwIn0seyJuYW1lIjoiZWtzX2FkbSIsImlkIjoiMCJ9LHsibmFtZSI6ImZnc19hZG0iLCJpZCI6IjAifSx7Im5hbWUiOiJjdHNfYWRtIiwiaWQiOiIwIn0seyJuYW1lIjoidnBjZXBfYWRtIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY3Nic19yZXBfYWNjZWxlcmF0aW9uIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWNzX2Rpc2tBY2MiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9kc3NfbW9udGgiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9vYnNfZGVlcF9hcmNoaXZlIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWNzX3Nwb3RfaW5zdGFuY2UiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9yZHNfbWFyaWFkYl9vYnQiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9iY3NfbmVzX3NnIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfYV9jbi1zb3V0aC00YyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2RlY19tb250aF91c2VyIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfaW50bF9vYSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Nicl9zZWxsb3V0IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZmxvd19jYSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Vjc19vbGRfcmVvdXJjZSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3dlbGlua2JyaWRnZV9lbmRwb2ludF9idXkiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9lY3AiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jYnJfZmlsZSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2lkbWVfbGlua3hfZm91bmRhdGlvbiIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Rtcy1yb2NrZXRtcTUtYmFzaWMiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9kbXMta2Fma2EzIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfc250OWJpbmwiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lZGdlc2VjX29idCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX29ic19kdWFsc3RhY2siLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9vYnNfZGVjX21vbnRoIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY3Nic19yZXN0b3JlIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfYmNwX3Byb2plY3QiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3NfYzZhIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfRUNfT0JUIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfa29vcGhvbmUiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9maW5lX2dyYWluZWQiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9tdWx0aV9iaW5kIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfc21uX2NhbGxub3RpZnkiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9vcmdpZF9jYSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfYXAtc291dGhlYXN0LTNkIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfaWFtX2lkZW50aXR5Y2VudGVyX2ludGwiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jc2JzX3Byb2dyZXNzYmFyIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfQmV0YSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Nlc19yZXNvdXJjZWdyb3VwX3RhZyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Vjc19vZmZsaW5lX2FjNyIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2V2c19yZXR5cGUiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9pbnRlcm5hbCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2tvb21hcCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2V2c19lc3NkMiIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2V2c19wb29sX2NhIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfcGVkYV9zY2hfY2EiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9hX2NuLXNvdXRod2VzdC0yYiIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2h3Y3BoIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfZWNzX29mZmxpbmVfZGlza180IiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfaHdkZXYiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9vcF9nYXRlZF9jYmhfdm9sdW1lIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfc21uX3dlbGlua3JlZCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2RhdGFhcnRzaW5zaWdodCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2h2X3ZlbmRvciIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3Vjc19vbl9hd3NfaW50bCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfY24tbm9ydGgtNGUiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF93YWZfY21jIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfYV9jbi1ub3J0aC00ZCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2Vjc19hYzciLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9jc2JzX3Jlc3RvcmVfYWxsIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfcmRzX21hcmlhZGJfb2J0X0ludGwiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lZHMiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9pYW1faWRlbnRpdHljZW50ZXJfY24iLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9hX2NuLW5vcnRoLTRmIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfb2EiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9zZnNfbGlmZWN5Y2xlIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfb3BfZ2F0ZWRfcm91bmR0YWJsZSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfYXAtc291dGhlYXN0LTFlIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfYV9ydS1tb3Njb3ctMWIiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9hX2FwLXNvdXRoZWFzdC0xZCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfYXAtc291dGhlYXN0LTFmIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfc21uX2FwcGxpY2F0aW9uIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfY3NlX2dhdGV3YXkiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9zbnQ5Ymk2bCIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX3JhbSIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX29yZ2FuaXphdGlvbnMiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3NfZ3B1X2c1ciIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX29wX2dhdGVkX21lc3NhZ2VvdmVyNWciLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9yaV9kd3MiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9lY3NfcmkiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9tZ2MiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9zbnQ5YiIsImlkIjoiMCJ9LHsibmFtZSI6Im9wX2dhdGVkX2FfcnUtbm9ydGh3ZXN0LTJjIiwiaWQiOiIwIn0seyJuYW1lIjoib3BfZ2F0ZWRfcmFtX2ludGwiLCJpZCI6IjAifSx7Im5hbWUiOiJvcF9nYXRlZF9pZWZfcGxhdGludW0iLCJpZCI6IjAifSx7Im5hbWUiOiI1OCw3NSwxNDQsNzIsMTQsMzgsMTUwLDgxLDEyNSw3LDE1OSwxMDAxLDExMSw5NiwzIiwiaWQiOiI4In0seyJuYW1lIjoiMTEsMTQiLCJpZCI6IjkifV0sImlzc3VlZF9hdCI6IjIwMjMtMDgtMjlUMDc6MzI6MDkuMTEyMDAwWiIsInVzZXIiOnsiZG9tYWluIjp7Inhkb21haW5fdHlwZSI6IkhXQ19ISyIsIm5hbWUiOiJBUENsb3VkZGVtb01NIiwiaWQiOiIwNTYwM2QwYmI1ODAxMGY3MGYyOGMwMTE1MDZkNThhMCIsInhkb21haW5faWQiOiI0NDUyNTNmNTRhMDg0NzFkYjA3ZTJiZTE0MTlhOTdhYyJ9LCJuYW1lIjoiR2VldGhha2EiLCJwYXNzd29yZF9leHBpcmVzX2F0IjoiIiwiaWQiOiI4NjI3NzA5ZDQwNGQ0ZThlOTI2MzVjYjY1N2Q1N2QxMiJ9fX0xggHBMIIBvQIBATCBlzCBiTELMAkGA1UEBhMCQ04xEjAQBgNVBAgMCUd1YW5nRG9uZzERMA8GA1UEBwwIU2hlblpoZW4xLjAsBgNVBAoMJUh1YXdlaSBTb2Z0d2FyZSBUZWNobm9sb2dpZXMgQ28uLCBMdGQxDjAMBgNVBAsMBUNsb3VkMRMwEQYDVQQDDApjYS5pYW0ucGtpAgkA3LMrXRBhahAwCwYJYIZIAWUDBAIBMA0GCSqGSIb3DQEBAQUABIIBABE+jEPgox7rUXPAo9iQtV6cjaj37p4AotigGrrW-u5E26tmzLuiJ9IjgmiVN0gRJEGWGDoElLmL6sQpA6Uv5X74ryCk4Qb44aZpODv6cJlzluofxEFVCqnVKqq4BaLcx3GXVcixJE7ejLS4OpWE52ID-NJUuA35UNW6SrUQlK4Y2SWKtBSdIqgbTsTgHOSUcXOjcKfLiQ6YfK1qinytL0bRTeDboVBzWZGJf2yUZ9OYvP0VeREw2-J2n5sPl4MKAqX87Q0D6lrkjt+-f8h70PbPG714pSM7WHZEfYa2OIZAYIWaWeit1mcepDc5KqQITz66JJRyBAO-yxAyUCcSZT8="
}

query_json_body = {
    "projects": [
        "0581f497e80026722f86c0110831c8d8",
        "05603d0bc78010f72f2bc01184bd43e5", 
        "0581e40cf28026752fc7c011929dae66",
        "057fd557628010e02ff1c01121650dca",
        "afb6d37800fa45e4b88c2f1063a195e0", 
        "0581f498478025052f57c01172200a56",
        "06c9c164a70026422f90c011d33994e9",
        "0581f4984380267a2f43c011700afdb8", 
        "076b162d080025132f80c0110fc4bcaf",
        "0581e3f62d800f6a2f6cc0114fdb4bb7",
        "0ed51bbef78090082f06c01151ed17aa", 
        "da449e406520447fbbb2ec6ee87ee055",
        "062216504e0026bd2f97c011f50d7e77",
        "0681115e3c0025a12fcbc0113b42fbf3", 
        "06aa42acdf8025502f93c0111c69b40c",
        "364c4fac5281410c937e7ea924e326ce",
    ],
    "resource_types": [
        "disk", "ecs", "scaling_group", "images", "vpcs", "security-groups",
        "shared_bandwidth", "eip", "cdn", "rds", "dcs", "dds", "cce-cluster",
        "aadinstance", "dedicated-host-tags", "dlv-instance", "app", "smn_topic",
        "apm", "nosql", "res-workspace", "dayu-instance", "projectman_project",
        "DNS_public_zone", "DNS_private_zone", "DNS_ptr_record", "graphs",
        "stream", "bcs", "vault", "bms_server", "ddm", "waf-instance", "waf",
        "waf-domain", "waf-bandwidth", "css-cluster", "dws_clusters", "clusters",
        "sfs", "sfs-turbo", "aom_resource_group", "loadbalancers", "cdm-clusters",
        "bucket", "nat_gateways", "kafka", "rabbitmq", "cci_namespace", "hss",
        "supportplan", "apig", "kms", "functions", "roma-instances", "roma-tasks",
        "gaussdb", "gcs_environment", "CES-alarm", "CES-dashboard",
        "CES-resourceGroup", "topics", "cc", "bwp", "cloudDataGuard", "sync",
        "migration", "backupMigration", "subscription", "cloudsite",
        "dc-directconnect", "dc-vgw", "dc-vif", "vpn-ngfw-gateway", "asm-mesh",
        "scm", "evaluate", "migrate", "dss", "dss_disk", "auditInstance",
        "dedicated-cluster-tags"
    ]
}

response = requests.post(query_url, json=query_json_body, headers=query_headers)

if response.status_code == 200:
    print("API call successful")
    # Parse the JSON response
    json_data = response.json()

    output_file_path = "output.json"

    with open(output_file_path, "w") as outfile:
        json.dump(json_data, outfile, indent=4)

    print(f"JSON response saved to {output_file_path}")

    resource_type_mapping = {
        "ecs": "huaweicloud_compute_instance",
        "vpcs": "huaweicloud_vpc",
        "security-groups": "huaweicloud_networking_secgroup",
        "subnet": "huaweicloud_vpc_subnet",
        "eip": "huaweicloud_vpc_eip",
        "loadbalancers": "huaweicloud_lb_loadbalancer",
        "images": "huaweicloud_images_image",
        "cce-cluster": "huaweicloud_cce_cluster",
        "bms_server": "huaweicloud_bms_instance",
        "disk": "huaweicloud_evs_volume",
        "scaling_group": "huaweicloud_as_group",
        "shared_bandwidth": "huaweicloud_vpc_bandwidth",
        "cdn": "huaweicloud_cdn_domain",
        "rds": "huaweicloud_rds_instance",
        "dcs": "huaweicloud_dcs_instance",
        "dds": "huaweicloud_dds_instance",
        "aadinstance": "huaweicloud_aad_forward_rule",
        #"dlv-instance": "",
        #"app": "",
        "smn_topic": "huaweicloud_smn_topic",
        #"apm": "",
        "nosql": "huaweicloud_gaussdb_mongo_instance",
        #"nosql": "huaweicloud_gaussdb_cassandra_instance",
        #"nosql": "huaweicloud_gaussdb_redis_instance",
        #"res-workspace": "",
        #"dayu-instance": "",
        "projectman_project": "huaweicloud_codearts_project",
        "DNS_public_zone": "huaweicloud_dns_zone",
        "DNS_private_zone": "huaweicloud_dns_zone",
        "DNS_ptr_record": "huaweicloud_dns_ptrrecord",
        "graphs": "huaweicloud_ges_graph",
        "stream": "huaweicloud_dis_stream",
        "bcs": "huaweicloud_bcs_instance",
        "vault": "huaweicloud_cbr_vault",
        "ddm": "huaweicloud_ddm_instance",
        "waf-instance": "huaweicloud_waf_cloud_instance",
        #"waf": "",
        "waf-domain": "huaweicloud_waf_domain",
        #"waf-bandwidth": "",
        "css-cluster": "huaweicloud_css_cluster",
        "dws_clusters": "huaweicloud_dws_cluster",
        "clusters": "huaweicloud_mapreduce_cluster",
        "sfs": "huaweicloud_sfs_file_system",
        "sfs-turbo": "huaweicloud_sfs_turbo",
        #"aom_resource_group": "",
        "cdm-clusters": "huaweicloud_cdm_cluster",
        "bucket": "huaweicloud_obs_bucket",
        "nat_gateways": "huaweicloud_nat_gateway",
        "kafka": "huaweicloud_dms_kafka_instance",
        "rabbitmq": "huaweicloud_dms_rabbitmq_instance",
        "cci_namespace": "huaweicloud_cci_namespace",
        #"hss": "",
        #"supportplan": "",
        "apig": "huaweicloud_apig_instance",
        "kms": "huaweicloud_kms_key",
        "functions": "huaweicloud_fgs_function",
        #"roma-instances": "",
        #"roma-tasks": "",
        "gaussdb": "huaweicloud_gaussdb_mysql_instance",
        #"gaussdb": "huaweicloud_gaussdb_opengauss_instance",
        #"gcs_environment": "",
        "CES-alarm": "huaweicloud_ces_alarmrule",
        #"CES-dashboard": "",
        "CES-resourceGroup": "huaweicloud_ces_resource_group",
        #"topics": "huaweicloud_lts_stream",
        "cc": "huaweicloud_cc_connection",
        "bwp": "huaweicloud_cc_bandwidth_package",
        # "cloudDataGuard": "",
        # "sync": "",
        # "migration": "",
        # "backupMigration": "",
        # "subscription": "",
        #"cloudsite": "",
        #"dc-directconnect": "",
        "dc-vgw": "huaweicloud_drs_job",
        "dc-vif": "huaweicloud_dc_virtual_interface",
        "vpn-ngfw-gateway": "huaweicloud_vpn_gateway",
        #"asm-mesh": "",
        "scm": "huaweicloud_scm_certificate",
        # "evaluate": "",
        # "migrate": "",
        # "dss": "",
        # "dss_disk": "",
        "auditInstance": "huaweicloud_dbss_instance",
        #"dedicated-cluster-tags": ""

    }
    
    if not os.path.exists("tf_configs"):
        os.makedirs("tf_configs")

    dict = {}
    dictIdx = {}

    for resource in json_data["resources"]:
        resource_id = resource["resource_id"]
        resource_type = resource["resource_type"]
        project_name = resource["project_name"]

        if resource_type in resource_type_mapping:
            terraform_term = resource_type_mapping[resource_type]
            
            dict.setdefault(project_name, {})
            project_dict = dict[project_name]

            dict[project_name].setdefault(resource_type, [])
            project_resources = project_dict[resource_type]

            dict[project_name][resource_type].append({
                "id": resource_id,
                "term": terraform_term
            })

    for project_name, project_dict in dict.items():
        project_folder = os.path.join("tf_configs", project_name)
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)

        fileOut = os.path.join(project_folder, "import.tf")

        static_terraform_config = (
            'terraform {\n'
            'required_providers {\n'
            'huaweicloud = {\n'
            'source  = "huaweicloud/huaweicloud"\n'
            'version = ">= 1.6.0"\n'
            '}\n'
            '}\n'
            '}\n\n'
            '# Configure the HuaweiCloud Provider\n'
            'provider "huaweicloud" {\n'
            'region     = "'+ project_name +'"\n'
            'access_key = "CDFYRVWI6RZVLWYPVY0M"\n'
            'secret_key = "A0U1YivtYl8Rfk8Dea8WwHi2oyiSg0npTEqac8rq"\n'
            '}\n'
        )

        dynamic_terraform_config = ""

        for resource_type, resources in project_dict.items():
            for resource_info in resources:
                resource_id = resource_info["id"]
                terraform_term = resource_info["term"]

                dictIdx.setdefault(resource_type, 0)
                dictIdx[resource_type] += 1
                idx = dictIdx[resource_type]
                
                module_config = (
                    'import {\n'
                    'id = "' + resource_id + '"\n'
                    'to = ' + terraform_term + '.imported_' + resource_type + str(idx) + '\n'
                    '}\n'
                )
                dynamic_terraform_config += module_config


        terraform_config = static_terraform_config + dynamic_terraform_config

        with open(fileOut, "w") as outfile:
            outfile.write(terraform_config)

        print(f"Terraform configuration for region '{project_name}' saved to {fileOut}")

else:
    print(f"API call failed with status code: {response.status_code}")
    print(response.text)


user_input = input("Do you want to continue with Phase 2 (Terraform commands) for all projects (y/n)? ").strip().lower()

if user_input == 'y':
    print("continue")