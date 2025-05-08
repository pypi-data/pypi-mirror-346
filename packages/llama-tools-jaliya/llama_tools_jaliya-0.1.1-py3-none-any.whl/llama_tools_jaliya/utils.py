import shutil
import os
from pathlib import Path


def clean_build_dirs():
    paths = ["llama.cpp/build", "models"]
    removed = []

    for path in paths:
        full_path = Path(path)
        if full_path.exists():
            shutil.rmtree(full_path)
            removed.append(str(full_path))

    if removed:
        print(f"Removed: {', '.join(removed)}")
    else:
        print("Nothing to clean.")


def show_status():
    llama_repo = Path("llama.cpp")
    build_dir = llama_repo / "build"
    models_dir = Path("models")
    venv_dir = Path.home() / "llama-cpp-venv"

    def check(path, description):
        exists = "exits" if path.exists() else "doesn't exists"
        print(f"{exists} {description}: {path}")

    print("Environment Status:")
    check(llama_repo, "llama.cpp repo")
    check(build_dir, "llama.cpp build")
    check(models_dir, "Models directory")
    check(venv_dir, "Virtual environment")
