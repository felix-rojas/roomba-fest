import importlib
import subprocess
import sys

dependencies = ["mesa", "numpy", "pandas"]


def install_and_import(needed_package):
    try:
        importlib.import_module(needed_package)
    except ImportError:
        print(f"{needed_package} is not installed, installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", needed_package])
        print(f"{needed_package} has been installed")


def get_packages():
    for package in dependencies:
        install_and_import(package)
