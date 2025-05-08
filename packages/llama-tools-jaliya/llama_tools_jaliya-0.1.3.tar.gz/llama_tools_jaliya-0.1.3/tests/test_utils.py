import unittest
from unittest.mock import patch
from llama_tools_jaliya import clean_build_dirs, show_status

class TestUtils(unittest.TestCase):
    @patch("llama_tools_jaliya.utils.shutil.rmtree")
    @patch("llama_tools_jaliya.utils.Path.exists", return_value=True)
    def test_clean_build_dirs(self, mock_exists, mock_rmtree):
        clean_build_dirs()
        self.assertTrue(mock_rmtree.called)

    @patch("llama_tools_jaliya.utils.Path.exists", return_value=True)
    def test_show_status(self, mock_exists):
        show_status()
        self.assertTrue(mock_exists.called)
