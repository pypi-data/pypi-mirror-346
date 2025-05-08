import os

import os

def add_app_to_installed_apps(app_name, settings_module_path):
    # Convert module path (e.g., myproject.settings or myproject.settings.base) to a file path
    parts = settings_module_path.split(".")
    if parts[-1] == "base":
        filepath = os.path.join(*parts) + ".py"
    else:
        # Check if it's a split settings structure with __init__.py pointing to base.py
        maybe_base_path = os.path.join(*parts, "base.py")
        if os.path.isfile(maybe_base_path):
            filepath = maybe_base_path
        else:
            filepath = os.path.join(*parts) + ".py"

    if not os.path.isfile(filepath):
        print(f"⚠️ Settings file not found at {filepath}")
        return

    with open(filepath, "r") as f:
        lines = f.readlines()

    installed_apps_start = None
    installed_apps_end = None

    for i, line in enumerate(lines):
        if "INSTALLED_APPS" in line and "=" in line:
            installed_apps_start = i
            break

    if installed_apps_start is None:
        print("❌ Could not find INSTALLED_APPS in the settings file.")
        return

    for j in range(installed_apps_start, len(lines)):
        if lines[j].strip().endswith("]"):
            installed_apps_end = j
            break

    if installed_apps_end is None:
        print("❌ Could not determine end of INSTALLED_APPS")
        return

    for k in range(installed_apps_start, installed_apps_end + 1):
        if f"'{app_name}'" in lines[k] or f'"{app_name}"' in lines[k]:
            print(f"ℹ️ {app_name} is already in INSTALLED_APPS")
            return

    indent = " " * 4
    lines.insert(installed_apps_end, f"{indent}'{app_name}',\n")

    with open(filepath, "w") as f:
        f.writelines(lines)

    print(f"✅ Added '{app_name}' to INSTALLED_APPS in {filepath}")

