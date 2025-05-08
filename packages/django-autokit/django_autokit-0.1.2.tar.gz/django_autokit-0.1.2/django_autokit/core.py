import subprocess
import os
from django_autokit.utils.env_loader import load_env_from_project_root
from django_autokit.utils.app_file_creator import create_files_for_app
from django_autokit.utils.settings_modifier import add_app_to_installed_apps
from django_autokit.utils.settings_splitter import split_settings


def handle_startapp(app_name):
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