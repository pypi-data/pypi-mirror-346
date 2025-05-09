from dotenv import load_dotenv, find_dotenv
import os

def find_settings_path():
    """Search for split or flat settings and return the appropriate import path (dot notation)."""
    for root, dirs, files in os.walk(os.getcwd()):
        # Prioritize split settings structure
        if "base.py" in files and os.path.basename(root) == "settings":
            rel_path = os.path.relpath(root, start=os.getcwd())
            module_path = rel_path.replace(os.sep, ".")
            return module_path

    # Fallback to classic settings.py
    for root, dirs, files in os.walk(os.getcwd()):
        if "settings.py" in files and "__init__.py" in files:
            if "migrations" not in root:
                rel_path = os.path.relpath(os.path.join(root, "settings.py"), start=os.getcwd())
                return rel_path.replace(os.sep, ".").replace(".py", "")
    return None

def ensure_env_file_exists():
    """Ensure .env exists and contains SETTINGS_PATH (with comment if newly added)."""
    env_path = os.path.join(os.getcwd(), ".env")
    guessed_path = find_settings_path()

    if not os.path.exists(env_path):
        # Create new .env with SETTINGS_PATH and helpful comment
        with open(env_path, "w") as f:
            f.write("# Path to your Django settings.py file\n")
            f.write("# Please verify that this path is correct:\n")
            if guessed_path:
                f.write(f"SETTINGS_PATH={guessed_path}\n")
                print(f"✅ Created .env and guessed SETTINGS_PATH: {guessed_path}")
            else:
                f.write("SETTINGS_PATH=\n")
                print("⚠️  Created .env but couldn't guess SETTINGS_PATH.")
    else:
        # Modify existing .env only if SETTINGS_PATH is missing
        with open(env_path, "r") as f:
            lines = f.readlines()

        if not any(line.strip().startswith("SETTINGS_PATH=") for line in lines):
            with open(env_path, "a") as f:
                f.write("\n# Path to your Django settings.py file\n")
                f.write("# Please verify that this path is correct:\n")
                if guessed_path:
                    f.write(f"SETTINGS_PATH={guessed_path}\n")
                    print(f"✅ Added SETTINGS_PATH to existing .env: {guessed_path}")
                else:
                    f.write("SETTINGS_PATH=\n")
                    print("⚠️  Added SETTINGS_PATH to .env but couldn't guess the path.")
        else:
            print("ℹ️  SETTINGS_PATH already exists in .env.")

def load_env_from_project_root():
    ensure_env_file_exists()
    
    env_path = find_dotenv(usecwd=True)
    if not env_path:
        print("⚠️  .env file not found in this or parent directories.")
        return False
    load_dotenv(dotenv_path=env_path)
    return True