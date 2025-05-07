# src/core/venv_management.py
import os
import sys
import shutil
import subprocess
from .exceptions import VenvCreationError, VenvPathError

def create_or_get_venv_paths(env_name="env", force_recreate=False, use_current_env=False):
    """
    Creates or gets paths for a Python virtual environment.

    Returns:
        tuple: (activate_script_path, python_executable_path, pip_command_list)
               Returns (None, sys.executable, [sys.executable, "-m", "pip"]) if use_current_env is True.
    Raises:
        VenvCreationError: If venv creation fails.
        VenvPathError: If essential venv executables are not found.
    """
    if use_current_env:
        print("Using current Python environment.")
        python_executable = sys.executable
        pip_command_list = [sys.executable, "-m", "pip"]

        if not os.path.exists(python_executable):
            raise VenvPathError(f"Current Python executable not found at {python_executable}")

        print(f"  Python: {python_executable}")
        print(f"  Pip command: {' '.join(pip_command_list)}")
        return None, python_executable, pip_command_list

    env_path = env_name
    if force_recreate and os.path.exists(env_path) and os.path.isdir(env_path):
        print(f"Force recreating virtual environment: Deleting existing '{env_path}'...")
        try:
            shutil.rmtree(env_path)
            print(f"Deleted '{env_path}'.")
        except OSError as e:
            raise VenvCreationError(f"Error deleting existing virtual environment '{env_path}': {e}")

    if not os.path.exists(env_path):
        print(f"Creating virtual environment '{env_path}'...")
        try:
            process = subprocess.run([sys.executable, "-m", "venv", env_path],
                                     check=True, capture_output=True, text=True)
            print(f"Virtual environment '{env_path}' created successfully.")
        except subprocess.CalledProcessError as e:
            stderr_msg = f"\nStderr: {e.stderr.strip()}" if e.stderr else ""
            raise VenvCreationError(f"Error creating virtual environment: {e}{stderr_msg}")
        except FileNotFoundError:
            raise VenvCreationError(f"Error: '{sys.executable}' not found. Cannot create virtual environment.")

    if os.name == "nt":
        activate_script = os.path.join(env_path, "Scripts", "activate")
        python_executable = os.path.join(env_path, "Scripts", "python.exe")
        pip_executable = os.path.join(env_path, "Scripts", "pip.exe")
    else:
        activate_script = os.path.join(env_path, "bin", "activate")
        python_executable = os.path.join(env_path, "bin", "python")
        pip_executable = os.path.join(env_path, "bin", "pip")

    if not os.path.exists(python_executable):
        raise VenvPathError(f"Python executable not found at {python_executable} in venv '{env_path}'")
    if not os.path.exists(pip_executable):
        raise VenvPathError(f"pip executable not found at {pip_executable} in venv '{env_path}'")

    return activate_script, python_executable, [pip_executable]