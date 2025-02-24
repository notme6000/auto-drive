#!/usr/bin/env python3

import os
import subprocess
import sys

VENV_PATH = "/home/notme6000/my-projects/python-projects/python-auto-drive/env"

MAIN_SCRIPT = "/home/notme6000/my-projects/python-projects/python-auto-drive/main.py"

def activate_virtualenv():
    
    if not os.path.exists(os.path.join(VENV_PATH, "bin", "activate")):
        print(f"error: virtula env not found")
        sys.exit(1)
        
    os.environ["VIRTUAL_ENV"] = VENV_PATH
    os.environ["PATH"] = f"{VENV_PATH}/bin:" + os.environ["PATH"]
    
def run_main_script():
    if not os.path.exists(MAIN_SCRIPT):
        print(f"error: main script not found")
        sys.exit(1)
    
    try:
        result = subprocess.run(["python3", MAIN_SCRIPT], capture_output=True, text=True)
        if result.returncode == 0:
            print("script executed successfully")
            print(result.stdout)
        else:
            print("Error during script execution:")
            print("STDOUT:")
            print(result.stdout)
            print("STDERR:")
            print(result.stderr, file=sys.stderr)
            sys.exit(result.returncode)
    except Exception as e:
        print(f"error while running the script: {e}")
        sys.exit(1)
        
def main():
    activate_virtualenv()
    run_main_script()
    
if __name__ == "__main__":
    main()
    
    