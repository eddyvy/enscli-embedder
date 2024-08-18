import unittest
from unittest.mock import call, patch, MagicMock
from file_embedder.file_parser.upload_llama_parse import upload_llama_parse_pdf
from file_embedder.file_parser.parsing_params import ParsingParams
from requests_toolbelt.multipart.encoder import MultipartEncoder

class TestUploadLlamaParsePDF(unittest.TestCase):

    @patch("file_embedder.file_parser.upload_llama_parse.time.sleep")
    @patch("file_embedder.file_parser.upload_llama_parse.requests.request")
    @patch("file_embedder.file_parser.upload_llama_parse.os.getenv")
    def test_upload_llama_parse_pdf_success(self, mock_getenv, mock_request, mock_sleep: MagicMock):
        mock_getenv.return_value = "fake_api_key"
        mock_response_post = MagicMock()
        mock_response_post.json.return_value = {"id": "12345", "status": "PENDING"}
        mock_response_post.raise_for_status = MagicMock()
        mock_response_get = MagicMock()
        mock_response_get.json.side_effect = [
            {"id": "12345", "status": "PENDING"},
            {"id": "12345", "status": "SUCCESS"}
        ]
        mock_response_get.raise_for_status = MagicMock()
        mock_request.side_effect = [mock_response_post, mock_response_get, mock_response_get]
        mock_sleep.return_value = None

        file_content = b"%PDF-1.4..."
        file_name = "test.pdf"
        parsing_params = ParsingParams()
        parsing_params.set_param("parsing_instruction", "test_parsing_instruction")
        parsing_params.set_param("lang", "en")

        fields = {
            "file": (file_name, file_content, "application/pdf"),
            "parsing_instruction": "test_parsing_instruction",
            "lang": "en"
        }
    
        result = upload_llama_parse_pdf(file_content, file_name, parsing_params)

        self.assertEqual(result, "12345")

        mock_getenv.assert_called_once_with("LLAMA_CLOUD_API_KEY")

        self.assertEqual(mock_request.call_count, 3)
        _, first_call_kwargs = mock_request.call_args_list[0]
        _, second_call_kwargs = mock_request.call_args_list[1]
        _, third_call_kwargs = mock_request.call_args_list[2]

        self.assertEqual(first_call_kwargs["method"], "POST")
        self.assertEqual(first_call_kwargs["url"], "https://api.cloud.llamaindex.ai/api/v1/parsing/upload")
        self.assertEqual(first_call_kwargs["headers"], {
            "Content-Type": "multipart/form-data",
            "Accept": "application/json",
            "Authorization": "Bearer fake_api_key"
        })

        boundary = first_call_kwargs["data"].split(b'\r\n')[0].decode().strip('--')
        self.assertEqual(first_call_kwargs["data"], MultipartEncoder(fields=fields, boundary=boundary).to_string())

        self.assertEqual(second_call_kwargs["method"], "GET")
        self.assertEqual(second_call_kwargs["url"], "https://api.cloud.llamaindex.ai/api/v1/parsing/job/12345")
        self.assertEqual(second_call_kwargs["headers"], {
            "Accept": "application/json",
            "Authorization": "Bearer fake_api_key"
        })

        self.assertEqual(third_call_kwargs["method"], "GET")
        self.assertEqual(third_call_kwargs["url"], "https://api.cloud.llamaindex.ai/api/v1/parsing/job/12345")
        self.assertEqual(third_call_kwargs["headers"], {
            "Accept": "application/json",
            "Authorization": "Bearer fake_api_key"
        })

        self.assertEqual(mock_sleep.call_count, 2)
        mock_sleep.assert_has_calls([call(2), call(2)])

        mock_response_post.raise_for_status.assert_called_once()
        mock_response_get.raise_for_status.assert_called()

    @patch("file_embedder.file_parser.upload_llama_parse.time.sleep")
    @patch("file_embedder.file_parser.upload_llama_parse.requests.request")
    @patch("file_embedder.file_parser.upload_llama_parse.os.getenv")
    def test_upload_llama_parse_pdf_success_with_empty_parsing_params(self, mock_getenv, mock_request, mock_sleep: MagicMock):
        mock_getenv.return_value = "fake_api_key"
        mock_response_post = MagicMock()
        mock_response_post.json.return_value = {"id": "12345", "status": "PENDING"}
        mock_response_get = MagicMock()
        mock_response_get.json.side_effect = [
            {"id": "12345", "status": "PENDING"},
            {"id": "12345", "status": "SUCCESS"}
        ]
        mock_request.side_effect = [mock_response_post, mock_response_get, mock_response_get]
        mock_sleep.return_value = None

        file_content = b"%PDF-1.4..."
        file_name = "test.pdf"
        parsing_params = ParsingParams()

        fields = {
            "file": (file_name, file_content, "application/pdf")
        }
    
        result = upload_llama_parse_pdf(file_content, file_name, parsing_params)

        self.assertEqual(result, "12345")

        mock_getenv.assert_called_once_with("LLAMA_CLOUD_API_KEY")

        self.assertEqual(mock_request.call_count, 3)
        _, first_call_kwargs = mock_request.call_args_list[0]
        _, second_call_kwargs = mock_request.call_args_list[1]
        _, third_call_kwargs = mock_request.call_args_list[2]

        self.assertEqual(first_call_kwargs["method"], "POST")
        self.assertEqual(first_call_kwargs["url"], "https://api.cloud.llamaindex.ai/api/v1/parsing/upload")
        self.assertEqual(first_call_kwargs["headers"], {
            "Content-Type": "multipart/form-data",
            "Accept": "application/json",
            "Authorization": "Bearer fake_api_key"
        })

        boundary = first_call_kwargs["data"].split(b'\r\n')[0].decode().strip('--')
        self.assertEqual(first_call_kwargs["data"], MultipartEncoder(fields=fields, boundary=boundary).to_string())

        self.assertEqual(second_call_kwargs["method"], "GET")
        self.assertEqual(second_call_kwargs["url"], "https://api.cloud.llamaindex.ai/api/v1/parsing/job/12345")
        self.assertEqual(second_call_kwargs["headers"], {
            "Accept": "application/json",
            "Authorization": "Bearer fake_api_key"
        })

        self.assertEqual(third_call_kwargs["method"], "GET")
        self.assertEqual(third_call_kwargs["url"], "https://api.cloud.llamaindex.ai/api/v1/parsing/job/12345")
        self.assertEqual(third_call_kwargs["headers"], {
            "Accept": "application/json",
            "Authorization": "Bearer fake_api_key"
        })

        self.assertEqual(mock_sleep.call_count, 2)
        mock_sleep.assert_has_calls([call(2), call(2)])

    @patch("file_embedder.file_parser.upload_llama_parse.requests.request")
    @patch("file_embedder.file_parser.upload_llama_parse.os.getenv")
    def test_upload_llama_parse_pdf_no_api_key(self, mock_getenv, mock_request):
        mock_getenv.return_value = None

        file_content = b"%PDF-1.4..."
        file_name = "test.pdf"
        parsing_params = ParsingParams()

        with self.assertRaises(EnvironmentError) as context:
            upload_llama_parse_pdf(file_content, file_name, parsing_params)

        self.assertEqual(str(context.exception), "LLAMA_CLOUD_API_KEY environment variable is not set")
        mock_getenv.assert_called_once_with("LLAMA_CLOUD_API_KEY")
        mock_request.assert_not_called()

    @patch("file_embedder.file_parser.upload_llama_parse.requests.request")
    @patch("file_embedder.file_parser.upload_llama_parse.os.getenv")
    def test_upload_llama_parse_pdf_failed_upload(self, mock_getenv, mock_request):
        mock_getenv.return_value = "fake_api_key"
        mock_response_post = MagicMock()
        mock_response_post.json.return_value = {"status": "ERROR"}
        mock_request.side_effect = [mock_response_post]

        file_content = b"%PDF-1.4..."
        file_name = "test.pdf"
        parsing_params = ParsingParams()

        with self.assertRaises(ValueError) as context:
            upload_llama_parse_pdf(file_content, file_name, parsing_params)

        self.assertEqual(str(context.exception), "Failed to obtain uploaded id file from LLAMA Cloud")

        mock_getenv.assert_called_once_with("LLAMA_CLOUD_API_KEY")
        self.assertEqual(mock_request.call_count, 1)

    @patch("file_embedder.file_parser.upload_llama_parse.time.sleep")
    @patch("file_embedder.file_parser.upload_llama_parse.requests.request")
    @patch("file_embedder.file_parser.upload_llama_parse.os.getenv")
    def test_upload_llama_parse_pdf_error_afer_pending(self, mock_getenv, mock_request, mock_sleep: MagicMock):
        mock_getenv.return_value = "fake_api_key"
        mock_response_post = MagicMock()
        mock_response_post.json.return_value = {"id": "12345", "status": "PENDING"}
        mock_response_get = MagicMock()
        mock_response_get.json.side_effect = [
            {"id": "12345", "status": "PENDING"},
            {"id": "12345", "status": "ERROR"}
        ]
        mock_request.side_effect = [mock_response_post, mock_response_get, mock_response_get]
        mock_sleep.return_value = None

        file_content = b"%PDF-1.4..."
        file_name = "test.pdf"
        parsing_params = ParsingParams()
        parsing_params.set_param("parsing_instruction", "test_parsing_instruction")
        parsing_params.set_param("lang", "en")
    
        with self.assertRaises(ValueError) as context:
            upload_llama_parse_pdf(file_content, file_name, parsing_params)

        self.assertEqual(str(context.exception), "Failed to parse PDF file with LLAMA Cloud")

    @patch("file_embedder.file_parser.upload_llama_parse.time.sleep")
    @patch("file_embedder.file_parser.upload_llama_parse.requests.request")
    @patch("file_embedder.file_parser.upload_llama_parse.os.getenv")
    def test_upload_llama_parse_pdf_error_infinite_pending(self, mock_getenv, mock_request, mock_sleep: MagicMock):
        mock_getenv.return_value = "fake_api_key"
        mock_response_post = MagicMock()
        mock_response_post.json.return_value = {"id": "12345", "status": "PENDING"}

        def side_effect():
            while True:
                yield {"id": "12345", "status": "PENDING"}

        mock_response_get = MagicMock()
        mock_response_get.json.side_effect = side_effect()

        mock_request.side_effect = [mock_response_post] + [mock_response_get] * 100
        mock_sleep.return_value = None

        file_content = b"%PDF-1.4..."
        file_name = "test.pdf"
        parsing_params = ParsingParams()
        parsing_params.set_param("parsing_instruction", "test_parsing_instruction")
        parsing_params.set_param("lang", "en")
    
        with self.assertRaises(ValueError) as context:
            upload_llama_parse_pdf(file_content, file_name, parsing_params)

        self.assertEqual(str(context.exception), "Max time exceeded to parse PDF file with LLAMA Cloud")
        self.assertEqual(mock_sleep.call_count, 60)
        self.assertEqual(mock_sleep.call_count, 60)

if __name__ == "__main__":
    unittest.main()
