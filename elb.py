import os
import json
import requests
import logging
from config import resource_type_mapping

logging.basicConfig(level=logging.INFO, format='%(message)s')

class ELBStatusFilter:
    def __init__(self):
        self.jsondumps_folder = 'jsondumps'
        self.tf_configs_folder = 'tf_configs'
        self.resource_count = {}

    def load_tokens(self):
        try:
            with open(os.path.join(self.jsondumps_folder, 'tokens.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"tokens.json not found in {self.jsondumps_folder}")
            raise

    def extract_loadbalancer_details(self):
        try:
            with open(os.path.join(self.jsondumps_folder, 'output.json'), 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            logging.error(f"output.json not found in {self.jsondumps_folder}")
            raise

        elb_details = {obj['resource_id']: {
            'project_name': obj['project_name'],
            'project_id': obj['project_id']} for obj in data['resources'] if obj['resource_type'] == 'loadbalancers'}

        if not elb_details:
            logging.warning("No loadbalancers found in the provided output.json")

        with open(os.path.join(self.jsondumps_folder, 'elb_details.json'), 'w') as f:
            json.dump(elb_details, f, indent=4)

        return elb_details

    def extract_elb_subresources(self, elb_status, project_name):
        loadbalancer_data = elb_status.get('statuses', {}).get('loadbalancer', {})
        
        for listener in loadbalancer_data.get('listeners', []):
            self.generate_tf_module('listeners', listener['id'], project_name)

            for pool in listener.get('pools', []):
                self.generate_tf_module('pools', pool['id'], project_name)

                for member in pool.get('members', []):
                    self.generate_tf_module('members', member['id'], project_name, pool_id=pool['id'])

                healthmonitor = pool.get('healthmonitor')
                if healthmonitor:
                    self.generate_tf_module('healthmonitor', healthmonitor['id'], project_name)

    def generate_tf_module(self, resource_type, resource_id, project_name, pool_id=None):
        if resource_type not in self.resource_count:
            self.resource_count[resource_type] = 0
        self.resource_count[resource_type] += 1

        terraform_term = resource_type_mapping.get(resource_type)
        if not terraform_term:
            return

        # Specialized template for members
        if resource_type == "members" and pool_id:
            resource_id = f"{pool_id}/{resource_id}"
            terraform_module = f"""
import {{
  id = "{resource_id}"
  to = {terraform_term}.imported_{resource_type}{self.resource_count[resource_type]}
}}"""
        # Default template for other resources
        else:
            terraform_module = f"""
import {{
  id = "{resource_id}"
  to = {terraform_term}.imported_{resource_type}{self.resource_count[resource_type]}
}}"""

        project_folder = os.path.join(self.tf_configs_folder, project_name)
        file_path = os.path.join(project_folder, 'import.tf')
        with open(file_path, 'a') as f:
            f.write(terraform_module)

    def fetch_elb_status(self, elb_details, tokens):
        statuses = {}
        api_versions = [2]

        for elb_name, details in elb_details.items():
            project_name = details['project_name']
            project_id = details['project_id']

            if project_name not in tokens:
                logging.warning(f"No token found for project {project_name}. Skipping {elb_name}.")
                continue

            token = tokens[project_name]
            headers = {"X-Auth-Token": token}

            for api_version in api_versions:
                url = f"https://elb.{project_name}.myhuaweicloud.com/v{api_version}/{project_id}/elb/loadbalancers/{elb_name}/statuses"
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    elb_status = response.json()
                    statuses[f"{elb_name}_v{api_version}"] = elb_status

                    self.extract_elb_subresources(elb_status, project_name)

                    logging.info(f"ELB API call successful for {project_name} with API version {api_version}")

                except requests.exceptions.RequestException as e:
                    logging.error(f"Error fetching data for {elb_name} with API version {api_version}: {e}")

        with open(os.path.join(self.jsondumps_folder, 'filtered_elb_statuses.json'), 'w') as f:
            json.dump(statuses, f, indent=4)

    def main(self):
        try:
            tokens = self.load_tokens()
            elb_details = self.extract_loadbalancer_details()
            if elb_details:
                self.fetch_elb_status(elb_details, tokens)
                logging.info(f"ELB statuses saved to {os.path.join(self.jsondumps_folder, 'filtered_elb_statuses.json')}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    elb_filter = ELBStatusFilter()
    elb_filter.main()
