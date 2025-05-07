# src/cli/main.py
import os
import sys
import argparse

# Remove src. prefix from imports since src is the package root
from core.venv_management import create_or_get_venv_paths
from core.package_management import (
    install_missing_packages,
    clear_environment_packages
)
from core.config import DEFAULT_IMPORT_TO_PACKAGE_MAP, DEFAULT_REQUIREMENTS_FILE
from core.exceptions import PyEnvRunnerError


def main():
    parser = argparse.ArgumentParser(
        description="Wrapper to manage Python venvs & run scripts, installing missing dependencies.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "script_path", nargs="?", default="main.py",
        help="Path to the Python script to run."
    )
    parser.add_argument(
        "--no-save-reqs", action="store_true",
        help="If set, newly installed packages will not be appended to the requirements file."
    )
    parser.add_argument(
        "--reqs-file", default=DEFAULT_REQUIREMENTS_FILE,
        help="Name of the requirements file."
    )
    parser.add_argument(
        "--use-current-env", action="store_true",
        help="Use the current Python environment instead of creating/using a virtual environment."
    )
    parser.add_argument(
        "--env-name", default="env",
        help="Name of the virtual environment directory. Ignored if --use-current-env is set."
    )
    parser.add_argument(
        "--force-recreate-env", action="store_true",
        help="Delete and recreate the virtual environment if it exists. Ignored if --use-current-env."
    )
    parser.add_argument(
        "--list-import-mappings", action="store_true",
        help="Print the predefined import-to-package mappings and exit."
    )
    parser.add_argument(
        "--clear-env", action="store_true",
        help="Remove all installed non-editable packages from the target environment and exit."
    )
    parser.add_argument(
        "--clear-env-no-confirm", action="store_true",
        help="Skip confirmation when clearing the environment (used with --clear-env)."
    )

    args = parser.parse_args()

    if args.list_import_mappings:
        print("--- Import to Package Mappings ---")
        for imp, pkg in DEFAULT_IMPORT_TO_PACKAGE_MAP.items():
            print(f"  {imp} -> {pkg}")
        print("----------------------------------")
        sys.exit(0)

    try:
        if args.clear_env:
            pip_to_use_for_clear = []
            env_description = ""
            if args.use_current_env:
                env_description = "current Python environment"
                print(f"Preparing to clear packages from the {env_description}.")
                pip_to_use_for_clear = [sys.executable, "-m", "pip"]
            else:
                env_dir_to_clear = args.env_name
                env_description = f"virtual environment: '{env_dir_to_clear}'"
                print(f"Preparing to clear packages from {env_description}.")
                if not os.path.isdir(env_dir_to_clear):
                    print(f"Virtual environment directory '{env_dir_to_clear}' does not exist. Nothing to clear.")
                    sys.exit(0)

                if os.name == "nt":
                    pip_exe_path = os.path.join(env_dir_to_clear, "Scripts", "pip.exe")
                else:
                    pip_exe_path = os.path.join(env_dir_to_clear, "bin", "pip")

                if not os.path.exists(pip_exe_path):
                    print(f"Pip executable not found at '{pip_exe_path}' in venv '{env_dir_to_clear}'. Cannot clear.")
                    sys.exit(1) # Or raise an exception
                pip_to_use_for_clear = [pip_exe_path]

            print(f"Target for clearing: {env_description}")
            clear_environment_packages(pip_to_use_for_clear, no_confirm=args.clear_env_no_confirm)
            sys.exit(0)

        target_script_path = args.script_path
        if not os.path.exists(target_script_path):
            print(f"Error: Target script '{target_script_path}' not found.")
            sys.exit(1) # Or raise an exception

        activate_script_path, venv_python_path, venv_pip_command_list = create_or_get_venv_paths(
            env_name=args.env_name,
            force_recreate=args.force_recreate_env,
            use_current_env=args.use_current_env
        )

        if not args.use_current_env and activate_script_path:
            print(f"\nVirtual environment is ready in './{args.env_name}'.")
            print(f"To activate it manually in your shell:")
            # Generate path relative to current working directory if possible
            try:
                rel_activate_path = os.path.relpath(activate_script_path, os.getcwd())
            except ValueError: # Happens if paths are on different drives on Windows
                rel_activate_path = activate_script_path

            if os.name == 'nt':
                print(f"  {rel_activate_path}")
            else:
                print(f"  source {rel_activate_path}")
            print("-" * 30)
        elif args.use_current_env:
            print("\nRunning in current Python environment. No venv activation needed by this script.")
            print("-" * 30)

        should_save_requirements = not args.no_save_reqs
        install_missing_packages(
            target_script_path,
            DEFAULT_IMPORT_TO_PACKAGE_MAP,
            venv_python_path,
            venv_pip_command_list,
            should_save_requirements,
            requirements_file_name=args.reqs_file
        )

    except PyEnvRunnerError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        # import traceback
        # traceback.print_exc() # For debugging unexpected errors
        sys.exit(1)

    print("\nWrapper script finished.")


if __name__ == "__main__":
    main()