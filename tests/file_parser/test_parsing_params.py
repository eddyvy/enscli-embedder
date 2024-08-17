import unittest
from file_embedder.file_parser.parsing_params import ParsingParams

class TestController(unittest.TestCase):
    def test_set_param_template(self):
        params = ParsingParams()
        params.set_param("template", "test_template")
        self.assertEqual(params.get_template(), "test_template")

    def test_set_param_lang(self):
        params = ParsingParams()
        params.set_param("lang", "en")
        self.assertEqual(params.get_lang(), "en")

    def test_set_param_regex(self):
        params = ParsingParams()
        params.set_param("regex", r"\d+")
        self.assertEqual(params.get_regex().pattern, r"\d+")

if __name__ == "__main__":
    unittest.main()
