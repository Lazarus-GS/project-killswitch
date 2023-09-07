import requests, os, json, logging
from user import username, password, domain
from config import mappedRegion
from utils import Loader, signalHandler

logging.basicConfig(level=logging.INFO, format='%(message)s')
loader = Loader(3, 0.5)

class SubnetFilter:
    def __init__(self):
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
            filtered_subnet_data[region_name] = {}
            for subnet in region_subnets['subnets']:
                vpc_id = subnet['vpc_id']
                subnet_id = subnet['id']
                if vpc_id in vpc_data:
                    project_name = vpc_data[vpc_id]
                    if region_name not in filtered_subnet_data:
                        filtered_subnet_data[region_name] = {}
                    filtered_subnet_data[region_name][subnet_id] = project_name

        return filtered_subnet_data
    
    def generate_terraform_modules(self, output_folder, filtered_subnet_data):
        for region_name, subnet_data in filtered_subnet_data.items():
            if not subnet_data:
                continue
            project_folder = os.path.join(output_folder, region_name)
            if not os.path.exists(project_folder):
                os.makedirs(project_folder)

            import_tf_file = os.path.join(project_folder, "import.tf")

            dynamic_terraform_config_subnet = ""
            dictIdx_sn = {}

            for subnet_id, _ in subnet_data.items():
                dictIdx_sn.setdefault(region_name, 0)
                dictIdx_sn[region_name] += 1
                idx = dictIdx_sn[region_name]

                module_config_subnet = (
                    'import {\n'
                    f'id = "{subnet_id}"\n'
                    f'to = huaweicloud_vpc_subnet.imported_subnet{idx}\n'
                    '}\n'
                )

                dynamic_terraform_config_subnet += module_config_subnet

            with open(import_tf_file, "a") as import_file:
                import_file.write(dynamic_terraform_config_subnet)

            logging.info(f"Terraform modules of subnets for region '{region_name}' saved to {import_tf_file}")

    def main(self):
        subnet_data = {}

        for region_name, region_id in mappedRegion.items():
            auth_token_project = self.authenticate_project(region_name)
            subnets = self.get_subnets(auth_token_project, region_name, region_id)
            subnet_data[region_name] = subnets
        logging.info("API calls for all subnets completed") 


        with open('subnets.json', 'w') as json_file:
            json.dump(subnet_data, json_file, indent=4)

        logging.info("\nSubnets saved to subnets.json")

        with open('output.json') as f:
            output_data = json.load(f)

        vpc_data = self.filter_vpcs(output_data)
        with open('filtered_vpc.json', 'w') as jsonVpc:
            json.dump(vpc_data, jsonVpc, indent=4)

        # Filter subnets based on vpc_data
        filtered_subnet_data = self.filter_subnets(subnet_data, vpc_data)

        # Save filtered subnets to filtered_subnets.json
        with open('filtered_subnets.json', 'w') as f:
            json.dump(filtered_subnet_data, f, indent=4)
        
        tf_configs_output_folder = "tf_configs"
        self.generate_terraform_modules(tf_configs_output_folder, filtered_subnet_data)

if __name__ == "__main__":
    subnet_filter = SubnetFilter()
    subnet_filter.main()
