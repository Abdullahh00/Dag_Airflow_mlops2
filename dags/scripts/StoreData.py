import os
import subprocess

class DVCManager:
    def __init__(self, remote_name, remote_url):
        self.remote_name = remote_name
        self.remote_url = remote_url

    def setup_dvc_remote(self):
        # Check if the remote is already configured
        result = subprocess.run("dvc remote list", shell=True, text=True, capture_output=True)
        if self.remote_name in result.stdout:
            print(f"DVC remote '{self.remote_name}' is already configured.")
        else:
            # Add the remote
            subprocess.run(f"dvc remote add -d {self.remote_name} {self.remote_url}", shell=True, check=True)
            print(f"DVC remote '{self.remote_name}' configured with URL: {self.remote_url}")

class DataVersionController:
    def __init__(self, filename):
        self.filename = filename
        self.dvc_manager = DVCManager('myremote', 'gdrive://1vREVD0UCDFbGtozg6BLWNEwGdw6pY1k5')

    def track_file_with_dvc(self):
        print(f"Starting DVC and Git operations for {self.filename}")
        
        # Ensure that the file is tracked by DVC
        if not os.path.exists('.dvc'):
            subprocess.run('dvc init --subdir', shell=True, check=True)
            print("DVC initialized.")

        # Configure DVC remote if not already configured
        self.dvc_manager.setup_dvc_remote()
        
        # Add the file to DVC tracking
        subprocess.run(f'dvc add {self.filename}', shell=True, check=True)
        print(f"{self.filename} added to DVC.")

        # Commit changes to git
        subprocess.run(f'git add {self.filename}.dvc .gitignore', shell=True, check=True)
        subprocess.run(f'git commit -m "Add/update {self.filename}"', shell=True, check=True)
        print("Changes committed to Git.")

        # Push the file to the DVC remote
        subprocess.run('dvc push', shell=True, check=True)
        print("Data pushed to DVC remote.")

def main():
    filename = 'data/extracted_data.json'
    print("Current Working Directory:", os.getcwd())
    print("File to be version-controlled:", filename)

    # Ensure file exists before attempting to add to DVC or Git
    if os.path.exists(filename):
        dvc_controller = DataVersionController(filename)
        dvc_controller.track_file_with_dvc()
    else:
        print(f"Error: The specified file {filename} does not exist.")

if __name__ == "__main__":
    main()
