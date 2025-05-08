# llama_tools/setup_llama.py

import subprocess
import os
from llama_tools_jaliya.venv import create_virtualenv

# Directory where llama.cpp will be cloned and built
repo_dir = "llama.cpp"

def clone_llama_cpp(repo_url="https://github.com/ggerganov/llama.cpp.git", repo_dir=repo_dir):
    """
    Clones the llama.cpp repository if it doesn't already exist.
    Also initializes and updates any Git submodules required by the repo.
    """
    if not os.path.exists(repo_dir):
        # Clone the repository from GitHub
        subprocess.run(["git", "clone", repo_url], check=True)
        print("Repository cloned.")
    else:
        print("Repository already exists, skipping clone.")

    # Initialize and update submodules
    subprocess.run(["git", "submodule", "update", "--init", "--recursive"], cwd=repo_dir, check=True)
    print("Submodules initialized.")

def setup_llama(jobs: int = 4, create_venv: bool = False):
    """
    Configures and builds the llama.cpp project using CMake and Ninja.
    Optionally creates and sets up a Python virtual environment.
    
    Args:
        jobs (int): Number of parallel jobs to use during the build process.
        create_venv (bool): Whether to set up a Python virtual environment after building.
    """
    # Prepare the CMake configuration command with desired build options
    cmake_config_cmd = [
        "cmake",
        "-S", ".",                         # Source directory
        "-B", "build",                    # Build directory
        "-G", "Ninja",                    # Use Ninja as the build system
        "-DCMAKE_BUILD_TYPE=Release",     # Use release build
        "-DLLAMA_BUILD_TESTS=OFF",        # Disable test build
        "-DLLAMA_BUILD_EXAMPLES=ON",      # Enable examples
        "-DLLAMA_BUILD_SERVER=ON",        # Enable server build
        "-DLLAMA_CURL=OFF"                # Disable curl (optional dependency)
    ]

    # Run CMake to configure the build
    subprocess.run(cmake_config_cmd, cwd=repo_dir, check=True)
    print("CMake configuration completed.")

    # Build the project using Ninja with specified parallel jobs
    subprocess.run(["cmake", "--build", "build", "--config", "Release", f"-j{jobs}"], cwd=repo_dir, check=True)
    print(f"Build completed with -j{jobs}.")

    # Optionally create and initialize a virtual environment with dependencies
    if create_venv:
        create_virtualenv()
        print("Virtual environment created and requirements installed.")
        print("Run `source ~/llama-cpp-venv/bin/activate` to activate the virtual environment.")
