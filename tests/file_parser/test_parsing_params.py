import unittest
from file_embedder.file_parser.parsing_params import ParsingParams

class TestController(unittest.TestCase):
    def test_set_param_parsing_instruction(self):
        params = ParsingParams()
        params.set_param("parsing_instruction", "test_parsing_instruction")
        self.assertEqual(params.get_parsing_instruction(), "test_parsing_instruction")

    def test_set_param_lang(self):
        params = ParsingParams()
        params.set_param("lang", "en")
        self.assertEqual(params.get_lang(), "en")

if __name__ == "__main__":
    unittest.main()
