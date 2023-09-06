import requests
import json, os, sys
from user import username, password, domain
from config import mappedRegion
from utils import Loader, signalHandler

loader = Loader(3, 0.5)
signalHandler.register_signal_handler()
subnet_idx = {}

def authenticateProject(username, password, domain, region_name):
    auth_url = "https://iam.myhuaweicloud.com/v3/auth/tokens"
    
    headers = {
        "Content-Type": "application/json"
    }
    authBodyProject = {
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
                "project": {
                    "name": region_name
                }
            }
        }
    }
    responseSubnet = requests.post(auth_url, json=authBodyProject, headers=headers)
    
    if responseSubnet.status_code == 201:
        return responseSubnet.headers['X-Subject-Token']
    else:
        raise Exception("Failed to obtain authentication token.")

def get_subnets(authTokenProject, region_name, region_id):
    subnets_url = f"https://vpc.{region_name}.myhuaweicloud.com/v1/{region_id}/subnets"
    
    headers = {
        "X-Auth-Token": authTokenProject
    }
    
    responseSubnet = requests.get(subnets_url, headers=headers)
    
    if responseSubnet.status_code == 200:
        return responseSubnet.json()
    else:
        raise Exception(f"Failed to query subnets for project {region_name}.")

def generate_subnet_module(subnet, region_name):
    global subnet_idx

    subnet_id = subnet.get("id")
    vpc_id = subnet.get("vpc_id")

    # Initialize the index for this subnet type if it doesn't exist
    subnet_idx.setdefault(region_name, {})
    subnet_idx[region_name].setdefault(vpc_id, 0)

    # Increment the index for this subnet type
    subnet_idx[region_name][vpc_id] += 1

    idx = subnet_idx[region_name][vpc_id]

    dynamic_tf_module = (
        f'import {{\n'
        f'  id = "{subnet_id}"\n'
        f'  to = "huaweicloud_vpc_subnet.imported_subnet{idx}"\n'
        f'}}\n\n'
    )

    return dynamic_tf_module


def create_and_save_vpc_project_mapping(json_data):
    vpc_project_mapping = {}
    for resource in json_data["resources"]:
        resource_id = resource["resource_id"]
        resource_type = resource["resource_type"]
        project_name = resource["project_name"]
        if resource_type == "vpcs":
            vpc_project_mapping[resource_id] = project_name

    with open('vpc_project_mapping.json', 'w') as json_file:
        json.dump(vpc_project_mapping, json_file, indent=4)

def main():
    
    subnet_data = {}
    
    for region_name, region_id in mappedRegion.items():
        authTokenProject = authenticateProject(username, password, domain, region_name)
        subnets = get_subnets(authTokenProject, region_name, region_id)
        subnet_data[region_name] = subnets
    
    with open('subnets.json', 'w') as json_file:
        json.dump(subnet_data, json_file, indent=4)
    
    loader.stop()
    print("\n\033[92mSubnets saved to subnets.json\033[0m\n")

    if len(sys.argv) > 1:
        json_data = json.loads(sys.argv[1])
        create_and_save_vpc_project_mapping(json_data)

    create_and_save_vpc_project_mapping(json_data)
    relevant_subnet_ids = []
    with open('vpc_project_mapping.json', 'r') as json_file:
        vpc_project_mapping = json.load(json_file)
        for region_name, region_id in mappedRegion.items():
            for subnet in subnet_data.get(region_name, []):
                vpc_id = subnet.get("vpc_id")
                if vpc_id in vpc_project_mapping:
                    relevant_subnet_ids.append(subnet["id"])

    with open('relevant_subnets.json', 'w') as json_file:
        json.dump(relevant_subnet_ids, json_file, indent=4)

if __name__ == "__main__":
    main()
