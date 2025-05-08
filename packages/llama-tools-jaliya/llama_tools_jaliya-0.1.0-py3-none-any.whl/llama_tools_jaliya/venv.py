import subprocess
import os
from pathlib import Path


def create_virtualenv():
    venv_path = Path.home() / "llama-cpp-venv"
    python_in_venv = venv_path / "bin" / "python"

    # Create the virtual environment
    subprocess.run(["python3", "-m", "venv", str(venv_path)], check=True)
    print("Virtual environment creating.")

    # Upgrade pip, wheel, and setuptools
    subprocess.run([str(python_in_venv), "-m", "pip", "install", "--upgrade", "pip", "wheel", "setuptools"], check=True)
    print("pip, wheel, setuptools upgraded.")

    # Install requirements
    requirements_path = "llama.cpp/requirements/requirements-convert_hf_to_gguf.txt"
    subprocess.run([str(python_in_venv), "-m", "pip", "install", "--upgrade", "-r", requirements_path], check=True)
    print("Requirements installed successfully.")
