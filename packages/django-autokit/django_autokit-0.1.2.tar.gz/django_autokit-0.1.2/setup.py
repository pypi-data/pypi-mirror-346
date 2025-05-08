from setuptools import setup, find_packages

setup(
    name="django-autokit",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "djkit=django_autokit.cli:main",
        ],
    },
    description="Custom Django startapp with boilerplate files and settings integration",
    author="Adeniyi Oluwadamilare",
)
