# request bodies and mappings
from user import username, password, domain

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
                    "name": username,
                    "password": password,
                    "domain": {
                     "name": domain
                    }
                }
            }
        },
        "scope": {
            "domain": {
                "name": domain
            }
        }
    }
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

resource_type_mapping = {
        "ecs": "huaweicloud_compute_instance",
        "vpcs": "huaweicloud_vpc",
        "security-groups": "huaweicloud_networking_secgroup",
        "subnet": "huaweicloud_vpc_subnet",
        "eip": "huaweicloud_vpc_eip",
        "loadbalancers": "huaweicloud_lb_loadbalancer",
        "pools": "huaweicloud_elb_pool",
        "listeners": "huaweicloud_lb_listener",
        "healthmonitors": "huaweicloud_elb_monitor",
        "members": "huaweicloud_elb_member",
        #"images": "huaweicloud_images_image",
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

        #commented-out resources are not supported by terraform as of now

    }

mappedRegion = {
    "af-south-1": "0581f497e80026722f86c0110831c8d8",
    "ap-southeast-2": "0581e40cf28026752fc7c011929dae66",
    #"my-kualalumpur-1",
    "ap-southeast-3": "057fd557628010e02ff1c01121650dca",
    "ap-southeast-4": "afb6d37800fa45e4b88c2f1063a195e0",
    "cn-east-3": "06c9c164a70026422f90c011d33994e9",
    "cn-east-2": "0581f498478025052f57c01172200a56",
    "cn-north-1": "0581f4984380267a2f43c011700afdb8",
    "cn-north-4": "076b162d080025132f80c0110fc4bcaf",
    "cn-south-1": "0581e3f62d800f6a2f6cc0114fdb4bb7",
    "ap-southeast-1": "05603d0bc78010f72f2bc01184bd43e5",
    "cn-southwest-2": "0ed51bbef78090082f06c01151ed17aa",
    #"eu-west-101",
    #"eu-west-0",
    #"sa-argentina-1",
    #"sa-peru-1",
    "na-mexico-1": "0681115e3c0025a12fcbc0113b42fbf3",
    "la-north-2": "da449e406520447fbbb2ec6ee87ee055",
    "la-south-2": "062216504e0026bd2f97c011f50d7e77",
    "sa-brazil-1": "06aa42acdf8025502f93c0111c69b40c",
    #"ae-ad-1",
    #"me-east-1",
    "tr-west-1": "364c4fac5281410c937e7ea924e326ce"

    #commented-out regions have diffent api endpoints or forbidden access
}