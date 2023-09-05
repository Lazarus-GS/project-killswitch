import os
import subprocess
import shutil
import requests
import json, signal
import sys, time, threading
from config import auth_headers, resource_type_mapping
from config import auth_json_body, query_json_body
from user import idEntProject, nameEntProject

class HuaweiCloudAPI:
    def __init__(self, auth_url, query_url, auth_headers, auth_json_body):
        self.auth_url = auth_url
        self.query_url = query_url
        self.auth_headers = auth_headers
        self.auth_json_body = auth_json_body
        self.x_subject_token = None

    def authenticate(self):
        auth_response = requests.post(self.auth_url, json=self.auth_json_body, headers=self.auth_headers)
        if auth_response.status_code == 201:
            self.x_subject_token = auth_response.headers.get('X-Subject-Token')
            return True
        return False

    def query_resources(self, query_json_body):
        if self.x_subject_token:
            query_headers = {
                "Content-Type": "application/json",
                "X-Auth-Token": self.x_subject_token
            }

            response = requests.post(self.query_url, json=query_json_body, headers=query_headers)
            return response

    def saveJson(self, json_data, file_path):  
        with open(file_path, "w") as outfile:
            json.dump(json_data, outfile, indent=4)
        loader.stop()
        print(f"\033[92mResources saved to {file_path}\033[0m")

class TerraformConfigGenerator:
    def __init__(self, json_data, resource_type_mapping):
        self.json_data = json_data
        self.resource_type_mapping = resource_type_mapping

    def generate_config(self, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        dict = {}
        dictIdx = {}

        for resource in self.json_data["resources"]:
            resource_id = resource["resource_id"]
            resource_type = resource["resource_type"]
            project_name = resource["project_name"]

            if resource_type in self.resource_type_mapping:
                terraform_term = self.resource_type_mapping[resource_type]

                dict.setdefault(project_name, {})
                project_dict = dict[project_name]

                dict[project_name].setdefault(resource_type, [])
                project_resources = project_dict[resource_type]

                dict[project_name][resource_type].append({
                    "id": resource_id,
                    "term": terraform_term
                })

        for project_name, project_dict in dict.items():
            project_folder = os.path.join(output_folder, project_name)
            if not os.path.exists(project_folder):
                os.makedirs(project_folder)

            file_out = os.path.join(project_folder, "import.tf")

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
                'region     = "' + project_name + '"\n'
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

            with open(file_out, "w") as outfile:
                outfile.write(terraform_config)

            loader.stop()
            print(f"Terraform configuration for region '{project_name}' saved to {file_out}")


class Loader:
    def __init__(self, count, delay):
        self.count = count
        self.delay = delay
        self.running = False
        self.loader_thread = None

    def _animate(self):
        while self.running:
            for _ in range(self.count):
                for _ in range(3):
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    time.sleep(self.delay)
                sys.stdout.write('\b\b\b   \b\b\b')  # Clear three dots
                sys.stdout.flush()
                time.sleep(self.delay)

    def start(self, text):
        if not self.loader_thread:
            self.running = True
            sys.stdout.write(text)
            self.loader_thread = threading.Thread(target=self._animate)
            self.loader_thread.daemon = True
            self.loader_thread.start()

    def stop(self):
        if self.loader_thread:
            self.running = False
            self.loader_thread.join()
            self.loader_thread = None
            sys.stdout.write('\n')
            sys.stdout.flush()

loader = Loader(3, 0.5)

def signal_handler(sig, frame):
    print("\nExiting...")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

def main():

    loader.start(f"\nGetting resources from project '{nameEntProject}'")

    auth_url = "https://eps.myhuaweicloud.com/v3/auth/tokens"
    query_url = f"https://eps.myhuaweicloud.com/v1.0/enterprise-projects/{idEntProject}/resources/filter"

    huawei_cloud_api = HuaweiCloudAPI(auth_url, query_url, auth_headers, auth_json_body)
    if huawei_cloud_api.authenticate():
        response = huawei_cloud_api.query_resources(query_json_body)
        if response.status_code == 200:
            json_data = response.json()
            output_folder = "tf_configs"

            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)

            os.makedirs(output_folder)

            huawei_cloud_api.saveJson(json_data, "output.json")

            loader.start("\nGetting Subnet details")
            subprocess.run(["python3", "subnet.py"])

            loader.start("\nGenerating Terraform configurations")
            terraform_config_generator = TerraformConfigGenerator(json_data, resource_type_mapping)
            terraform_config_generator.generate_config(output_folder)
            loader.stop()
        else:
            loader.stop()
            print(f"API call failed with status code: {response.status_code}")
            print(response.text)
    else:
        loader.stop()
        print("Authentication failed.")

    user_input = input("\nDo you want to continue to Phase 2 (y/n)? ").lower()

    if user_input == 'y':
        print("\nContinuing to Phase 2...")
        subprocess.run(["python3", "tfcom.py"])
    elif user_input == 'n':
        print("Program terminated.")
    else:
        print("Invalid input. Program terminated.")

if __name__ == "__main__":
    main()
