import unittest
from unittest.mock import patch
from llama_tools_jaliya import create_virtualenv

class TestVirtualEnv(unittest.TestCase):
    @patch("llama_tools_jaliya.venv.subprocess.run")
    @patch("llama_tools_jaliya.venv.Path.exists", return_value=True)
    def test_create_virtualenv(self, mock_exists, mock_run):
        create_virtualenv()
        self.assertTrue(mock_run.called)
        self.assertEqual(mock_run.call_count, 3)
