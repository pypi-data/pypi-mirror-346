import subprocess
import os
import shutil
from huggingface_hub import Repository, whoami

def push_gguf(repo_id: str, gguf_path: str, local_repo_dir: str = "./hf_tmp_repo"):
    """
    Uploads a GGUF model file to the specified Hugging Face Hub repository.

    Args:
        repo_id (str): Hugging Face repo ID (e.g. "username/model-name")
        gguf_path (str): Path to the GGUF model file to upload
        local_repo_dir (str): Local directory to use for cloning the repo (default: "./hf_tmp_repo")
    """

    # Ensure user is authenticated with Hugging Face CLI
    try:
        whoami()
    except Exception:
        subprocess.run(["huggingface-cli", "login"], check=True)

    # Clone the repo if not already cloned, or pull latest changes
    if not os.path.isdir(os.path.join(local_repo_dir, ".git")):
        if os.path.exists(local_repo_dir):
            shutil.rmtree(local_repo_dir)  # Remove if directory exists but isn't a git repo
        repo = Repository(local_dir=local_repo_dir, clone_from=repo_id, use_auth_token=True)
    else:
        repo = Repository(local_dir=local_repo_dir)
        repo.git_pull()  # Sync with latest remote changes

    # Copy the GGUF model into the repo directory
    gguf_filename = os.path.basename(gguf_path)
    target_path = os.path.join(local_repo_dir, gguf_filename)
    shutil.copy(gguf_path, target_path)

    # Commit and push the GGUF model to Hugging Face Hub
    repo.push_to_hub(commit_message=f"Upload {gguf_filename}")
    print(f"Uploaded `{gguf_filename}` to https://huggingface.co/{repo_id}")
