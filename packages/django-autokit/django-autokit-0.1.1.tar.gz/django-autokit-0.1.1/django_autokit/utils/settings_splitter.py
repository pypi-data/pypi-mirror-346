import os
import shutil
from dotenv import load_dotenv

def split_settings():
    # Ensure the script is being run from the root of the Django project (where manage.py is located)
    root_dir = os.getcwd()
    manage_py_path = os.path.join(root_dir, "manage.py")

    if not os.path.isfile(manage_py_path):
        print("❌ 'manage.py' not found in the current directory. Please run this command from the root directory of your Django project.")
        return

    # Step 1: Locate settings.py
    settings_path = None
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "settings.py" in filenames:
            settings_path = os.path.join(dirpath, "settings.py")
            break

    if not settings_path:
        print("❌ Could not find settings.py")
        return

    project_dir = os.path.dirname(settings_path)
    settings_folder = os.path.join(project_dir, "settings")

    if os.path.exists(settings_folder):
        print("⚠️  settings/ folder already exists. Aborting split.")
        return

    os.makedirs(settings_folder)
    print(f"✅ Created folder: {settings_folder}")

    # Step 2: Backup the original settings.py by moving it to settings/settings_original.py
    original_backup_path = os.path.join(settings_folder, "settings_original.py")
    shutil.move(settings_path, original_backup_path)
    print(f"✅ Moved settings.py to {original_backup_path}")

    # Step 3: Create base.py from the original settings
    base_path = os.path.join(settings_folder, "base.py")
    with open(original_backup_path, "r") as original_file:
        content = original_file.read()
    with open(base_path, "w") as base_file:
        base_file.write(content)

    print(f"✅ Created base.py with the original settings content")

    # Step 4: Create dev.py and prod.py
    dev_path = os.path.join(settings_folder, "dev.py")
    prod_path = os.path.join(settings_folder, "prod.py")

    with open(dev_path, "w") as f:
        f.write("from .base import *\n\nDEBUG = True\n")
    with open(prod_path, "w") as f:
        f.write("from .base import *\n\nDEBUG = False\n")

    print("✅ Created dev.py and prod.py")

    # Step 5: Create __init__.py with .env ENV switch
    init_path = os.path.join(settings_folder, "__init__.py")
    with open(init_path, "w") as f:
        f.write("""import os
from dotenv import load_dotenv

load_dotenv()
env = os.getenv("ENV", "dev")

if env == "prod":
    from .prod import *
else:
    from .dev import *
""")
    print("✅ Created __init__.py with dynamic ENV loading")

    # Step 6: Add ENV=dev to .env if not already present
    env_file = os.path.join(root_dir, ".env")
    load_dotenv(env_file)
    if not os.getenv("ENV"):
        with open(env_file, "a") as f:
            f.write("\n# Set to 'prod' when deploying to a live server\n")
            f.write("ENV=dev\n")
        print("✅ Added ENV=dev to .env")
    else:
        print("ℹ️  ENV already exists in .env")
