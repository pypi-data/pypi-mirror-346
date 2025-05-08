# File: django_autokit/cli.py
import argparse
from django_autokit.core import handle_startapp, handle_split_settings, handle_generate_gitignore
from django_autokit.utils.env_loader import ensure_env_file_exists


def main():
    parser = argparse.ArgumentParser(
        description="Django Autokit - Automate Django project setup and maintenance."
    )
    
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: startapp
    startapp_parser = subparsers.add_parser("startapp", help="Create a Django app with boilerplate files.")
    startapp_parser.add_argument("app_name", help="Name of the Django app to create")

    # Subcommand: split-settings
    subparsers.add_parser("split-settings", help="Split settings.py into modular settings")

    # Subcommand: init-env
    subparsers.add_parser("init-env", help="Create or update .env with SETTINGS_PATH")

    # subcommand: gitignore
    subparsers.add_parser("gitignore", help="Generate a Django-friendly .gitignore")

    args = parser.parse_args()

    if args.command == "startapp":
        ensure_env_file_exists()
        handle_startapp(args.app_name)
    elif args.command == "split-settings":
        handle_split_settings()
    elif args.command == "init-env":
        ensure_env_file_exists()
    elif args.command == "gitignore":
        handle_generate_gitignore()
    else:
        parser.print_help()
