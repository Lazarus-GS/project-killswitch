import os
import subprocess, signal
from user import nameEntProject
from main import signal_handler

signal.signal(signal.SIGINT, signal_handler)

def execTf(command, project_folder, command_name):
    print(f"\033[0;34mRunning '{command_name}' in {project_folder}...\033[0m")

    process = subprocess.Popen(
        command, cwd=project_folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )

    while True:
        stdout_line = process.stdout.readline()
        stderr_line = process.stderr.readline()
        
        if not stdout_line and not stderr_line and process.poll() is not None:
            break
        
        if stdout_line:
            print(f"{stdout_line.strip()}")
        if stderr_line:
            print(f"{stderr_line.strip()}")

    process.wait()

    if process.returncode == 0:
        print(f"\033[93m'{command_name}' executed successfully in {project_folder}\033[0m")
    else:
        print(f"\033[91mError while executing '{command_name}' in {project_folder}\033[0m")

def tfcommands(base_folder):
    
    project_folders = [folder for folder in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, folder))]

    for project_folder in project_folders:
        project_path = os.path.join(base_folder, project_folder)
       
        initCommand = ['terraform', 'init']
        execTf(initCommand, project_path, 'terraform init')

        configPlanCommand = ['terraform', 'plan', '-generate-config-out=generated_output.tf']
        execTf(configPlanCommand, project_path, 'terraform -config plan')

        # planCommand = ['terraform', 'plan']
        # execTf(planCommand, project_path, 'terraform plan')

        # applyCommand = ['terraform', 'apply', '-auto-approve']
        # execTf(applyCommand, project_path, 'terraform apply')

        # destroyCommand = ['terraform', 'destroy', '-auto-approve']
        # execTf(destroyCommand, project_path, 'terraform destroy')

if __name__ == "__main__":
    base_folder = "tf_configs"
    tfcommands(base_folder)

print(f"\n\033[92mAll the resources in project '{nameEntProject}' are successfully deleted!\033[0m")
