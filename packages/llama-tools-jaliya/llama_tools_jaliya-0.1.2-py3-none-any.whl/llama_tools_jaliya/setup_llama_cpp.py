# llama_tools/setup_llama.py
import subprocess
import os
from llama_tools_jaliya.venv import create_virtualenv



repo_dir = "llama.cpp"

def clone_llama_cpp(repo_url="https://github.com/ggerganov/llama.cpp.git", repo_dir=repo_dir):
    if not os.path.exists(repo_dir):
        subprocess.run(["git", "clone", repo_url], check=True)
        print("Repository cloned.")
    else:
        print("Repository already exists, skipping clone.")

    subprocess.run(["git", "submodule", "update", "--init", "--recursive"], cwd=repo_dir, check=True)
    print("Submodules initialized.")



def setup_llama(jobs: int = 4, create_venv: bool = False):

    cmake_config_cmd = [
        "cmake",
        "-S", ".",
        "-B", "build",
        "-G", "Ninja",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DLLAMA_BUILD_TESTS=OFF",
        "-DLLAMA_BUILD_EXAMPLES=ON",
        "-DLLAMA_BUILD_SERVER=ON",
        "-DLLAMA_CURL=OFF"
    ]
    subprocess.run(cmake_config_cmd, cwd=repo_dir, check=True)
    print("CMake configuration completed.")

    subprocess.run(["cmake", "--build", "build", "--config", "Release", f"-j{jobs}"], cwd=repo_dir, check=True)
    print(f"Build completed with -j{jobs}.")

    if create_venv:
        create_virtualenv()
        print("Virtual environment created and requirements installed.")
        print("Run `source ~/llama-cpp-venv/bin/activate` to activate the virtual environment.")
