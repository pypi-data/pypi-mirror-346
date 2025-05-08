import os

FILES_TO_CREATE = [
    "utils.py",
    "signals.py",
    "context_processors.py",
    "urls.py",
    "forms.py",
    "serializers.py",
]

def create_files_for_app(app_name):
    app_path = os.path.join(os.getcwd(), app_name)
    if not os.path.isdir(app_path):
        print(f"App '{app_name}' not found at {app_path}")
        return

    for filename in FILES_TO_CREATE:
        file_path = os.path.join(app_path, filename)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(f"# {filename} for {app_name} app\n")
            print(f"Created: {file_path}")
        else:
            print(f"Already exists: {file_path}")
