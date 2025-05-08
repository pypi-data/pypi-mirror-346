# Django Autokit

**Django Autokit** is a CLI tool to automate the setup of a Django project. It helps with environment variable setup, settings splitting (`base.py`, `dev.py`, `prod.py`), `.env` scaffolding, and boilerplate app creation — saving you time when starting new projects.

---

## ✨ Features

- Automatically split `settings.py` into `base.py`, `dev.py`, and `prod.py`
- Create a `.env` file with `SETTINGS_PATH` and `ENV` variables
- Add newly created apps to `INSTALLED_APPS` (supports flat and split settings)
- Smart handling for Django 4.x and 5.x compatibility

---

## 📦 Installation

```bash
pip install django-autokit


🚀 Usage
1. Initialize in your Django project root:
bash
Copy
Edit
python -m django_autokit.cli
This will:

Detect or create .env

Set SETTINGS_PATH to the correct module path (e.g. yourproject.settings.base)

Add ENV=dev by default with a comment

Split your settings if needed


2. Create an app:
bash
Copy
Edit
python -m django_autokit.cli startapp blog
This will:

Create the blog app using Django’s startapp

Automatically add it to INSTALLED_APPS


⚙️ Environment Management
In your .env, you’ll find:

env
Copy
Edit
# Path to your Django settings file (use base.py for split settings)
SETTINGS_PATH=yourproject.settings.base

# Set ENV to 'prod' when deploying to production
ENV=dev


📁 Project Structure After Running Autokit
yourproject/
├── manage.py
├── .env
├── yourproject/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   └── ...
├── blog/
│   └── ...


✅ Compatibility
✅ Django 4.x

✅ Django 5.x

✅ Python 3.7+

🛡 License
This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing
Pull requests are welcome! Feel free to open an issue to suggest new features or report bugs.