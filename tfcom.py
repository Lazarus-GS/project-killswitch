import os
import subprocess
import logging

from user import nameEntProject
logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_terraform_command(command, project_folder, command_name, print_stdout = False):
    logging.info(f"\033[0;34mRunning '{command_name}' in {project_folder}...\033[0m")

    process = subprocess.run(
        command,
        cwd=project_folder,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    stdout = process.stdout
    stderr = process.stderr

    if process.returncode == 0:
        # logging.info(f"\033[93m'{command_name}' executed successfully in {project_folder}\033[0m")
        logging.info("\033[1m\033[92m✓\033[0m \033[1mDone\033[0m")
        if print_stdout:
            print(stdout)
    else:
        logging.error(f"\033[91mError while executing '{command_name}' in {project_folder}\033[0m")
        print(stderr)

def tf_commands(base_folder):
    project_folders = [
        folder for folder in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, folder))
    ]

    for project_folder in project_folders:
        project_path = os.path.join(base_folder, project_folder)

        init_command = ["terraform", "init"]
        run_terraform_command(init_command, project_path, "terraform init")

        config_plan_command = ["terraform", "plan", "-generate-config-out=generated_output.tf"]
        run_terraform_command(config_plan_command, project_path, "terraform plan")

        apply_command = ["terraform", "apply", "-auto-approve"]
        run_terraform_command(apply_command, project_path, "terraform apply",print_stdout = False)

        # destroy_command = ["terraform", "destroy", "-auto-approve"]
        # run_terraform_command(destroy_command, project_path, "terraform destroy")

if __name__ == "__main__":
    base_folder = "tf_configs"
    tf_commands(base_folder)

    print(f"\n\033[92mAll the resources in project '{nameEntProject}' are successfully deleted!\033[0m")
