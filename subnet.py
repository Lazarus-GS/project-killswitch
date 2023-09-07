import requests
import json
import logging
from user import username, password, domain
from config import mappedRegion
from utils import Loader, signalHandler

class SubnetFilter:
    def __init__(self):
        self.loader = Loader(3, 0.5)
        signalHandler.register_signal_handler()

    def authenticate_project(self, region_name):
        auth_url = "https://iam.myhuaweicloud.com/v3/auth/tokens"
        headers = {"Content-Type": "application/json"}
        auth_body_project = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": username,
                            "password": password,
                            "domain": {"name": domain}
                        }
                    }
                },
                "scope": {"project": {"name": region_name}}
            }
        }
        try:
            response_subnet = requests.post(auth_url, json=auth_body_project, headers=headers)
            response_subnet.raise_for_status()
            return response_subnet.headers['X-Subject-Token']
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to obtain authentication token: {e}")
            raise

    def get_subnets(self, auth_token_project, region_name, region_id):
        subnets_url = f"https://vpc.{region_name}.myhuaweicloud.com/v1/{region_id}/subnets"
        headers = {"X-Auth-Token": auth_token_project}
        try:
            response_subnet = requests.get(subnets_url, headers=headers)
            response_subnet.raise_for_status()
            return json.loads(response_subnet.text)
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to query subnets for project {region_name}: {e}")
            raise

    def filter_vpcs(self, output_data):
        vpc_data = {}
        for obj in output_data['resources']:
            if obj['resource_type'] == 'vpcs':
                vpc_data[obj['resource_id']] = obj['project_name']
        return vpc_data

    def filter_subnets(self, subnet_data, vpc_data):
        filtered_subnet_data = {}
        for region_name, region_subnets in subnet_data.items():
            for subnet in region_subnets['subnets']:
                vpc_id = subnet['vpc_id']
                if vpc_id in vpc_data:
                    project_name = vpc_data[vpc_id]
                    subnet_id = subnet['id']
                    filtered_subnet_data[subnet_id] = project_name
        return filtered_subnet_data

    def main(self):
        subnet_data = {}

        for region_name, region_id in mappedRegion.items():
            auth_token_project = self.authenticate_project(region_name)
            subnets = self.get_subnets(auth_token_project, region_name, region_id)
            subnet_data[region_name] = subnets

        with open('subnets.json', 'w') as json_file:
            json.dump(subnet_data, json_file, indent=4)

        self.loader.stop()
        logging.info("Subnets saved to subnets.json")

        with open('output.json') as f:
            output_data = json.load(f)

        vpc_data = self.filter_vpcs(output_data)

        filtered_subnet_data = self.filter_subnets(subnet_data, vpc_data)
        with open('filtered_subnets.json', 'w') as f:
            json.dump(filtered_subnet_data, f, indent=4)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    subnet_filter = SubnetFilter()
    subnet_filter.main()
