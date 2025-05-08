"""
This script launches the `llama-server` from the llama.cpp project using a specified GGUF model file.

Usage:
    python run_llama_server.py --gguf_model path/to/model.gguf

Requirements:
    - The llama.cpp repository must be cloned and built.
    - The `llama-server` binary must exist at: llama.cpp/build/bin/llama-server
    - A valid GGUF model must be provided via --gguf_model.

This is useful for quickly spinning up a local inference server for LLaMA models using the llama.cpp backend.
"""

import subprocess
import argparse
import os


def run_llama_server(gguf_model: str):
    llama_server_path = "llama.cpp/build/bin/llama-server"

    if not os.path.isfile(llama_server_path):
        raise FileNotFoundError(f"llama-server binary not found at expected path: {llama_server_path}")

    command = [
        llama_server_path,
        "-m", gguf_model
    ]

    print(f"Starting llama-server with model: {gguf_model}...")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to launch llama-server: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch llama-server with a GGUF model.")
    parser.add_argument("--gguf_model", required=True, help="Path to the GGUF model file.")

    args = parser.parse_args()

    run_llama_server(gguf_model=args.gguf_model)
