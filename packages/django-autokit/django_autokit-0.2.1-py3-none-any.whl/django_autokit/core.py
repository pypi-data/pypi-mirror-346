import subprocess
import os
import re
from django_autokit.utils.env_loader import load_env_from_project_root
from django_autokit.utils.app_file_creator import create_files_for_app
from django_autokit.utils.settings_modifier import add_app_to_installed_apps
from django_autokit.utils.settings_splitter import split_settings
from django_autokit.utils.gen_gitignore import generate_gitignore

def is_valid_app_name(name):
    # Valid app name in Django: lowercase, numbers, and underscores; cannot start with a number
    return bool(re.match(r"^[a-z_][a-z0-9_]*$", name))

def handle_startapp(app_name):
    # Validate the app name
    if not is_valid_app_name(app_name):
        print(f"Error: '{app_name}' is an invalid app name. It should only contain lowercase letters, numbers, and underscores, and cannot start with a number.")
        return  # Exit early if the app name is invalid
    
    """Handles creating a new app and adding boilerplate."""
    if not load_env_from_project_root():
        return

    settings_path = os.getenv("SETTINGS_PATH")
    if not settings_path:
        print("⚠️  SETTINGS_PATH not set in your .env file.")
        return

    subprocess.run(["python", "manage.py", "startapp", app_name])
    create_files_for_app(app_name)
    add_app_to_installed_apps(app_name, settings_path)

def handle_split_settings():
    """Handles splitting the settings.py into modular files."""
    split_settings()

def handle_generate_gitignore():
    generate_gitignore()