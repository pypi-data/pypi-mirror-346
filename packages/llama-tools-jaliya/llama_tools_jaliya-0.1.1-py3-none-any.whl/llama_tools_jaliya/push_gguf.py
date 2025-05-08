import subprocess
import os
import shutil
from huggingface_hub import Repository, whoami

def push_gguf(repo_id: str, gguf_path: str, local_repo_dir: str = "./hf_tmp_repo"):
    # Ensure logged in
    try:
        whoami()
    except Exception:  # broad catch, avoids version issues
        subprocess.run(["huggingface-cli", "login"], check=True)

    # Clone or pull
    if not os.path.isdir(os.path.join(local_repo_dir, ".git")):
        if os.path.exists(local_repo_dir):
            shutil.rmtree(local_repo_dir)
        repo = Repository(local_dir=local_repo_dir, clone_from=repo_id, use_auth_token=True)
    else:
        repo = Repository(local_dir=local_repo_dir)
        repo.git_pull()

    # Copy model
    gguf_filename = os.path.basename(gguf_path)
    target_path = os.path.join(local_repo_dir, gguf_filename)
    shutil.copy(gguf_path, target_path)

    # Push
    repo.push_to_hub(commit_message=f"Upload {gguf_filename}")
    print(f"Uploaded `{gguf_filename}` to https://huggingface.co/{repo_id}")
