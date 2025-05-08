import unittest
from unittest.mock import patch
from llama_tools_jaliya import run_llama_server

class TestRunServer(unittest.TestCase):
    @patch("llama_tools_jaliya.server.subprocess.run")
    @patch("llama_tools_jaliya.server.os.path.isfile", return_value=True)
    def test_run_llama_server_success(self, mock_isfile, mock_run):
        run_llama_server("model.gguf")
        mock_run.assert_called_once()
