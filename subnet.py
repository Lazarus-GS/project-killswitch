import requests
import json, signal
from user import username, password, domain
from config import mappedRegion
from utils import Loader, signalHandler

loader = Loader(3, 0.5)
signalHandler.register_signal_handler()

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

if __name__ == "__main__":
    main()
