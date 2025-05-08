# main.py
import sys
import os
import subprocess # For running git commands
import logging
from PySide6.QtWidgets import QApplication
# Ensure this import uses a relative path if main_window is in a subdirectory of the package
# For this example, assuming main_window.py is in a 'gui' subdirectory relative to main.py
# If main.py is the entry point of a package, and gui is a sub-package:
from .gui.main_window import MainWindow


def run_git_command(args, capture_output=False, check_errors=False):
    """Helper function to run git commands."""
    try:
        # Using a list of arguments is safer than shell=True
        command = ['git'] + args
        logging.debug(f"Running command: {' '.join(command)}")
        process = subprocess.run(
            command,
            capture_output=capture_output,
            text=True, # Decodes stdout/stderr as text
            check=check_errors # Raises CalledProcessError if git returns non-zero
        )
        return process
    except FileNotFoundError:
        logging.error("Git command not found. Please ensure Git is installed and in your system's PATH.")
        print("ERROR: Git command not found. Please ensure Git is installed and in your system's PATH.", file=sys.stderr)
        return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Git command failed: {e}")
        if e.stdout:
            logging.error(f"Git stdout: {e.stdout.strip()}")
        if e.stderr:
            logging.error(f"Git stderr: {e.stderr.strip()}")
        print(f"ERROR: Git command failed: {e}", file=sys.stderr)
        if e.stderr:
            print(f"Git stderr: {e.stderr.strip()}", file=sys.stderr)
        return None

def get_git_config_value(key):
    """Gets a global git config value."""
    process = run_git_command(['config', '--global', key], capture_output=True)
    if process and process.returncode == 0 and process.stdout.strip():
        return process.stdout.strip()
    # If the key is not set, git config returns exit code 1.
    # If git is not found, process will be None.
    return None

def set_git_config_value(key, value):
    """Sets a global git config value."""
    print(f"Attempting to set global Git config: {key} = \"{value}\"")
    process = run_git_command(['config', '--global', key, value], check_errors=False) # Don't raise, check returncode
    if process and process.returncode == 0:
        logging.info(f"Successfully set Git config: {key} = {value}")
        print(f"Successfully set global Git config: {key}")
        return True
    else:
        logging.error(f"Failed to set Git config: {key}")
        print(f"ERROR: Failed to set global Git config: {key}. Please do it manually.", file=sys.stderr)
        return False

def check_and_configure_git_identity():
    """Checks for global git user.name and user.email and prompts if not set."""
    print("Checking Git global configuration...")
    logging.info("Checking Git global configuration...")

    # First, check if git command itself is available
    git_version_process = run_git_command(['--version'])
    if not git_version_process: # git not found or other initial error
        return False # Error message already printed by run_git_command

    user_name = get_git_config_value('user.name')
    user_email = get_git_config_value('user.email')

    configured_successfully = True

    if not user_name:
        print("Global Git 'user.name' is not configured.")
        logging.warning("Global Git 'user.name' is not configured.")
        while True:
            name_input = input("Please enter your full name for Git commits: ").strip()
            if name_input:
                if not set_git_config_value('user.name', name_input):
                    configured_successfully = False
                    break # Break from while, config failed
                break
            else:
                print("Name cannot be empty. Please try again.")
        if not configured_successfully: return False
    else:
        print(f"Git user.name found: {user_name}")
        logging.info(f"Git user.name found: {user_name}")

    if not user_email:
        print("Global Git 'user.email' is not configured.")
        logging.warning("Global Git 'user.email' is not configured.")
        while True:
            email_input = input("Please enter your email address for Git commits: ").strip()
            if email_input: # Basic check, could add regex for more validation
                if not set_git_config_value('user.email', email_input):
                    configured_successfully = False
                    break # Break from while, config failed
                break
            else:
                print("Email cannot be empty. Please try again.")
        if not configured_successfully: return False
    else:
        print(f"Git user.email found: {user_email}")
        logging.info(f"Git user.email found: {user_email}")

    if configured_successfully:
        print("Git global user identity is configured.")
        logging.info("Git global user identity is configured.")
    else:
        print("There was an issue configuring Git. Please check messages above.", file=sys.stderr)
        logging.error("Failed to fully configure Git identity.")
    return configured_successfully


# Wrap the application startup logic in a main() function
def main():
    # Configure logging
    logging.basicConfig(
           level=logging.INFO,
           format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
           handlers=[
               logging.StreamHandler(sys.stdout), # Log to console
               # logging.FileHandler("app.log") # Optionally log to a file
           ]
       )

    # --- Git Configuration Check ---
    if not check_and_configure_git_identity():
        logging.critical("Essential Git configuration (user.name, user.email) is missing or could not be set. Exiting.")
        print("\nEssential Git configuration (user.name, user.email) is missing or could not be set.", file=sys.stderr)
        print("Please configure Git manually using:", file=sys.stderr)
        print("  git config --global user.name \"Your Name\"", file=sys.stderr)
        print("  git config --global user.email \"youremail@example.com\"", file=sys.stderr)
        print("And ensure Git is installed and in your system's PATH.", file=sys.stderr)
        sys.exit(1) # Exit with an error code
    # --- End Git Configuration Check ---

    app = QApplication(sys.argv)

    # Set application style and metadata
    app.setApplicationName("Git Made Simple")
    app.setOrganizationName("GitMadeSimple")

    # Create main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
