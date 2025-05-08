import unittest
from unittest.mock import patch
from llama_tools_jaliya import convert_model

class TestConvertModel(unittest.TestCase):
    @patch("llama_tools_jaliya.convert_and_quantize.subprocess.run")
    def test_convert_model_basic(self, mock_run):
        convert_model(
            hf_model="facebook/opt-125m",
            gguf_output="model.gguf"
        )
        self.assertTrue(mock_run.called)
