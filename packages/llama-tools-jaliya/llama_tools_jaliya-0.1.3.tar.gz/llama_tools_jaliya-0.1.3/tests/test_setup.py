import unittest
from unittest.mock import patch
from llama_tools_jaliya.setup_llama_cpp import setup_llama, clone_llama_cpp

class TestSetupLlama(unittest.TestCase):
    @patch("llama_tools_jaliya.setup_llama_cpp.subprocess.run")
    @patch("llama_tools_jaliya.setup_llama_cpp.os.path.exists", return_value=False)
    def test_clone_llama_cpp(self, mock_exists, mock_run):
        clone_llama_cpp()
        self.assertTrue(mock_run.called)
        mock_run.assert_any_call(["git", "clone", "https://github.com/ggerganov/llama.cpp.git"], check=True)

    @patch("llama_tools_jaliya.setup_llama_cpp.subprocess.run")
    def test_setup_llama(self, mock_run):
        setup_llama(jobs=2, create_venv=False)
        self.assertTrue(mock_run.called)
