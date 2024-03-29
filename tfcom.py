import os, re
import subprocess
import logging

from user import nameEntProject
logging.basicConfig(level=logging.INFO, format='%(message)s')

class PostConfig:
    """Post-processing configurations after generating Terraform files."""

    @staticmethod
    def ecsConflicts(folder_path):
        filename = os.path.join(folder_path, "generated_output.tf")

        with open(filename, 'r') as f:
            content = f.read()

        # Match ECS resource blocks
        ecs_pattern = r'(resource\s+"huaweicloud_compute_instance".*?})'
        ecs_blocks = re.findall(ecs_pattern, content, flags=re.DOTALL)

        for block in ecs_blocks:
            # Within each ECS block, comment out the security_groups line
            modified_block = re.sub(r'^(.*security_groups\s*=\s*\[.*\].*)$', r'#\1', block, flags=re.MULTILINE)
            content = content.replace(block, modified_block)

        with open(filename, 'w') as f:
            f.write(content)

def run_terraform_command(command, project_folder, command_name, print_stdout=False):
    logging.info(f"\033[0;34mRunning '{command_name}' in {project_folder}...\033[0m")

    if command_name == "terraform destroy":
        with subprocess.Popen(command, 
                              cwd=project_folder, 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              universal_newlines=True, 
                              bufsize=1) as process:

            while True:
                output_line = process.stdout.readline()
                if output_line:
                    print(output_line.strip())
                else:
                    break

            stderr = process.stderr.read()

            if process.returncode == 0:
                logging.info("\033[1m\033[92m✓\033[0m \033[1mDone\033[0m")
                if print_stdout and stderr:
                    print(stderr)
            else:
                logging.error(f"\033[91mError while executing '{command_name}' in {project_folder}\033[0m")
                if stderr:
                    print(stderr)
    else:
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
        run_terraform_command(config_plan_command, project_path, "terraform config plan")

        PostConfig.ecsConflicts(project_path)
        logging.info("\033[1m\033[92m✓\033[0m \033[1mPost Configs Done\033[0m")

        plan_command = ["terraform", "plan"]
        run_terraform_command(plan_command, project_path, "terraform plan")

        apply_command = ["terraform", "apply", "-auto-approve"]
        run_terraform_command(apply_command, project_path, "terraform apply")

        destroy_command = ["terraform", "destroy", "-auto-approve"]
        run_terraform_command(destroy_command, project_path, "terraform destroy",print_stdout = True)

if __name__ == "__main__":
    base_folder = "tf_configs"
    tf_commands(base_folder)

    print(f"\n\033[92mAll the resources in project '{nameEntProject}' are successfully deleted!\033[0m")
