import subprocess
import os
from pathlib import Path

def create_virtualenv():
    """
    Creates a Python virtual environment in ~/llama-cpp-venv,
    upgrades pip-related tools, and installs required dependencies.
    """
    venv_path = Path.home() / "llama-cpp-venv"
    python_in_venv = venv_path / "bin" / "python"

    # Step 1: Create the virtual environment
    print(f"Creating virtual environment at: {venv_path}")
    subprocess.run(["python3", "-m", "venv", str(venv_path)], check=True)
    print("Virtual environment created.")

    # Step 2: Upgrade pip, wheel, and setuptools
    print("Upgrading pip, wheel, and setuptools...")
    subprocess.run([str(python_in_venv), "-m", "pip", "install", "--upgrade", "pip", "wheel", "setuptools"], check=True)
    print("pip, wheel, setuptools upgraded.")

    # Step 3: Install project requirements
    requirements_path = "llama.cpp/requirements/requirements-convert_hf_to_gguf.txt"
    print(f"Installing requirements from: {requirements_path}")
    subprocess.run([str(python_in_venv), "-m", "pip", "install", "--upgrade", "-r", requirements_path], check=True)
    print("Requirements installed successfully.")
    print("Activate the (llama-cpp-venv)")
