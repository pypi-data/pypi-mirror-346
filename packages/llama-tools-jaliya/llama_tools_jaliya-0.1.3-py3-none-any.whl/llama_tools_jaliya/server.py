"""
Launches the `llama-server` from the llama.cpp project using a specified GGUF model file.

Usage:
    python run_llama_server.py --gguf_model path/to/model.gguf

Requirements:
    - llama.cpp must be cloned and built with the server enabled.
    - `llama-server` binary must exist at: llama.cpp/build/bin/llama-server
    - A valid GGUF model must be provided via --gguf_model

This script is useful for quickly launching a local inference server with a GGUF model
using the llama.cpp backend.
"""

import subprocess
import argparse
import os


def run_llama_server(gguf_model: str):
    """
    Launches llama-server with the specified GGUF model.

    Args:
        gguf_model (str): Path to the GGUF model file.
    """
    llama_server_path = "llama.cpp/build/bin/llama-server"

    if not os.path.isfile(llama_server_path):
        raise FileNotFoundError(f"Error: llama-server binary not found at: {llama_server_path}\n"
                                f"Make sure llama.cpp is built with server support.")

    command = [
        llama_server_path,
        "-m", gguf_model
    ]

    print(f"[INFO] Starting llama-server with model: {gguf_model} ...")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to launch llama-server:\n{e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run llama.cpp server with a GGUF model")
    parser.add_argument("--gguf_model", required=True, help="Path to the .gguf model file")

    args = parser.parse_args()

    run_llama_server(gguf_model=args.gguf_model)
