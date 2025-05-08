
# gguf-converter-huggingface

A Python package and CLI tool for building, converting, quantizing, and uploading [LLaMA](https://ai.meta.com/llama/) models using [`llama.cpp`](https://github.com/ggerganov/llama.cpp). Ideal for efficient local inference, edge deployment, and privacy-preserving LLM applications.

---

## What It Does

`llama-tools-jaliya` automates the full pipeline for preparing Hugging Face LLaMA models for `llama.cpp`. It helps you:

* Clone and build `llama.cpp`
* Convert HF models to GGUF format
* Quantize with precision options like `Q4_0`, `Q5_1`, `TQ1_0`, etc.
* Upload `.gguf` models to Hugging Face Hub
* Set up a Python virtual environment
* Run everything via CLI or Python API

---

## Installation

Install from PyPI:

```bash
pip install llama-tools-jaliya
```

---

## CLI Usage

```bash
llama-tools-jaliya <command> [options]
```

---

## Commands Overview

| Command      | Description                           | Python Function         |
| ------------ | ------------------------------------- | ----------------------- |
| `clone`      | Clone `llama.cpp` repo                | `clone_llama_cpp()`     |
| `setup`      | Build `llama.cpp` (CMake + Ninja)     | `setup_llama()`         |
| `venv`       | Create a Python virtual environment   | `create_virtualenv()`   |
| `convert`    | Convert HF model to GGUF and quantize | `convert_model(...)`    |
| `upload`     | Upload `.gguf` to Hugging Face        | `push_gguf(...)`        |
| `run-server` | Start local inference server          | `run_llama_server(...)` |
| `clean`      | Remove build and model folders        | `clean_build_dirs()`    |
| `status`     | Show build and env status             | `show_status()`         |

---

## Commands

### Clone `llama.cpp`

```bash
llama-tools-jaliya clone
```

---

### Build with CMake + Ninja

```bash
llama-tools-jaliya setup -j 8 --create-venv
```

> **Windows Users:** Install CMake, Ninja, Visual Studio Build Tools with C++ components. Use PowerShell or Git Bash.

Here’s the updated section with activation instructions for different operating systems:

---

### Create Virtual Environment

```bash
llama-tools-jaliya venv
```

Once created, activate the virtual environment:

**Linux / macOS (bash/zsh):**

```bash
source ~/llama-cpp-venv/bin/activate
```

**Windows (PowerShell):**

```powershell
~\llama-cpp-venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
%USERPROFILE%\llama-cpp-venv\Scripts\activate.bat
```

To deactivate the environment, simply run:

```bash
deactivate
```

---

Would you like me to add a check that prints these platform-specific instructions from within the CLI?


### Convert & Quantize HF Model

```bash
llama-tools-jaliya convert \
  --hf_model meta-llama/Llama-2-7b-hf \
  --gguf_output models/Llama-2-7b.gguf \
  --quantized_output models/Llama-2-7b-q4.gguf \
  --quant_type Q4_0 \
  --quant_algo 8
```

---

### Upload to Hugging Face

```bash
llama-tools-jaliya upload \
  --repo_id username/model-name \
  --gguf_path models/Llama-2-7b-q4.gguf
```

---

### Run Server

```bash
llama-tools-jaliya run-server --gguf_model models/Llama-2-7b-q4.gguf
```

---

### Clean Builds

```bash
llama-tools-jaliya clean
```

---

### Status Report

```bash
llama-tools-jaliya status
```

---

##  Supported Quantization Types

| Type     | Size / Description         |
| -------- | -------------------------- |
| `Q4_0`   | 4.34G, basic 4-bit         |
| `Q4_1`   | 4.78G, improved 4-bit      |
| `Q5_1`   | 5.65G, high-quality 5-bit  |
| `Q8_0`   | 7.96G, near full precision |
| `Q3_K_M` | 3.74G, 3-bit mixed         |
| `IQ2_XS` | 2.31 bpw                   |
| `TQ1_0`  | 1.69 bpw, ternary          |

See full list: [llama.cpp#quantization](https://github.com/ggerganov/llama.cpp#quantization)

---

##  Python API Usage

Import and use core functions programmatically:

```python
from llama_tools_jaliya import (
    setup_llama,
    convert_model,
    push_gguf,
    run_llama_server,
    clean_build_dirs,
    show_status
)
```

---

### `setup_llama(jobs=4, create_venv=False)`

Builds `llama.cpp`.

```python
setup_llama(jobs=8, create_venv=True)
```

---

### `convert_model(hf_model, gguf_output, quantized_output=None, quant_type=None, quant_algo="8")`

Converts a HF model to `.gguf` and applies quantization.

```python
convert_model(
    hf_model="meta-llama/Llama-2-7b-hf",
    gguf_output="models/7b.gguf",
    quantized_output="models/7b-q4.gguf",
    quant_type="Q4_0"
)
```

---

### `push_gguf(repo_id, gguf_path, local_repo_dir="./hf_tmp_repo")`

Uploads the quantized model.

```python
push_gguf("your-username/llama-7b-q4", "models/7b-q4.gguf")
```

---

### `run_llama_server(gguf_model)`

Launches a local server using a `.gguf` model.

```python
run_llama_server("models/7b-q4.gguf")
```

---

## 📁 Package Structure

```
llama_tools_jaliya/
├── __main__.py                  # CLI Entrypoint
├── setup_llama_cpp.py           # llama.cpp build logic
├── venv.py                      # Virtualenv setup
├── convert_and_quantize.py      # HF → GGUF conversion
├── push_gguf.py                 # Upload to Hugging Face
├── server.py                    # Run llama-server
├── utils.py                     # Clean, status reporting
```

---

##  Development

### Build & Publish

```bash
rm -rf dist/ build/ *.egg-info
python -m build
twine upload dist/*
```

### Run Tests

```bash
pytest tests/
```

---

## 📄 License

MIT License

---

## 👤 Author

**Jaliya Nimantha**
[jaliya@ahlab.org](mailto:jaliya@ahlab.org)
[ahlab.org](https://ahlab.org)

