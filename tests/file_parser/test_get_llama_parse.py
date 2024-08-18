import unittest
from unittest.mock import MagicMock, patch
from file_embedder.file_parser.get_llama_parse import get_llama_parse

class TestGetLlamaParse(unittest.TestCase):
    @patch("file_embedder.file_parser.get_llama_parse.requests.request")
    @patch("file_embedder.file_parser.get_llama_parse.os.getenv")
    def test_get_llama_parse_success(self, mock_getenv: MagicMock, mock_request: MagicMock):
        mock_getenv.return_value = "fake_api_key"

        job_id = "12345"
        expected_text = "Lorem ipsum dolor sit amet"

        mock_response = MagicMock()
        mock_response.json.return_value = {"text": expected_text}
        mock_response.raise_for_status = MagicMock()
        mock_request.return_value = mock_response

        result = get_llama_parse(job_id)

        mock_getenv.assert_called_once_with("LLAMA_CLOUD_API_KEY")
        mock_request.assert_called_once_with(
            "GET",
            f"https://api.cloud.llamaindex.ai/api/v1/parsing/job/{job_id}/result/text",
            headers={
                "Accept": "application/json",
                "Authorization": "Bearer fake_api_key"
            }
        )
        self.assertEqual(result, expected_text.encode("utf-8"))
        mock_response.raise_for_status.assert_called_once()

    @patch("file_embedder.file_parser.get_llama_parse.requests.request")
    @patch("file_embedder.file_parser.get_llama_parse.os.getenv")
    def test_get_llama_parse_error_no_api_key(self, mock_getenv: MagicMock, _: MagicMock):
        mock_getenv.return_value = ""

        with self.assertRaises(EnvironmentError) as context:
            get_llama_parse("12345")

        self.assertEqual(str(context.exception), "LLAMA_CLOUD_API_KEY environment variable is not set")

if __name__ == "__main__":
    unittest.main()