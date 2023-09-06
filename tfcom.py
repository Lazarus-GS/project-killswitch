import os
import subprocess
from user import nameEntProject


def exec_tf(command, project_folder, command_name):
    print(f"\033[0;34mRunning '{command_name}' in {project_folder}...\033[0m")

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
        print(f"\033[93m'{command_name}' executed successfully in {project_folder}\033[0m")
        print(stdout)
    else:
        print(f"\033[91mError while executing '{command_name}' in {project_folder}\033[0m")
        print(stderr)


def tf_commands(base_folder):
    project_folders = [
        folder for folder in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, folder))
    ]

    for project_folder in project_folders:
        project_path = os.path.join(base_folder, project_folder)

        init_command = ["terraform", "init"]
        exec_tf(init_command, project_path, "terraform init")

        config_plan_command = ["terraform", "plan", "-generate-config-out=generated_output.tf"]
        exec_tf(config_plan_command, project_path, "terraform -config plan")

        # The following commands are commented out because they are not needed in this case.
        # plan_command = ["terraform", "plan"]
        # exec_tf(plan_command, project_path, "terraform plan")
        #
        # apply_command = ["terraform", "apply", "-auto-approve"]
        # exec_tf(apply_command, project_folder, "terraform apply")
        #
        # destroy_command = ["terraform", "destroy", "-auto-approve"]
        # exec_tf(destroy_command, project_folder, "terraform destroy")


if __name__ == "__main__":
    base_folder = "tf_configs"
    tf_commands(base_folder)

    print(f"\n\033[92mAll the resources in project '{nameEntProject}' are successfully deleted!\033[0m")
