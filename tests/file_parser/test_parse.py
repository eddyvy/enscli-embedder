import io
import unittest
import azure.functions as func
from unittest.mock import ANY, patch, MagicMock

from requests_toolbelt import MultipartEncoder
from file_embedder.file_parser.parsing_params import ParsingParams
from file_embedder.file_request import FileRequest
from file_embedder.file_parser.parse import parse

@patch("file_embedder.file_parser.parse.upload_llama_parse_pdf")
@patch("file_embedder.file_parser.parse.get_llama_parse")
@patch("file_embedder.file_parser.parse.save_file")
class TestParse(unittest.TestCase):

    def test_parse_pdf(self, mock_save_file: MagicMock, mock_get_llama_parse: MagicMock, mock_upload_llama_parse_pdf: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.pdf", io.BytesIO(b"pdf content"), "application/json"),
                "project_name": "test_project",
                "parsing_param_1": "value_1",
                "parsing_param_2": "value_2"
            }
        )

        file_request = FileRequest(func.HttpRequest(
            method="POST",
            url="/api/embedder",
            headers={"Content-Type": multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        ))

        mock_upload_llama_parse_pdf.return_value = "test_job_id"
        mock_get_llama_parse.return_value = "parsed content"

        result = parse(file_request)

        mock_upload_llama_parse_pdf.assert_called_once_with(
            file_content=b"pdf content",
            file_name="test.pdf",
            parsing_params=ANY
        )
        expected_parsing_params = ParsingParams()
        actual_parsing_params = mock_upload_llama_parse_pdf.call_args[1]['parsing_params']
        self.assertEqual(actual_parsing_params.__dict__, expected_parsing_params.__dict__)

        mock_get_llama_parse.assert_called_once_with("test_job_id")
        mock_save_file.assert_called_once_with(
            content="parsed content",
            file_path="test_project/test_unfiltered.txt"
        )

        self.assertEqual(result, "parsed content")

    def test_parse_txt(self, mock_save_file: MagicMock, mock_get_llama_parse: MagicMock, mock_upload_llama_parse_pdf: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.txt", io.BytesIO(b"txt content"), "text/plain"),
                "project_name": "test_project"
            }
        )

        file_request = FileRequest(func.HttpRequest(
            method="POST",
            url="/api/embedder",
            headers={"Content-Type": multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        ))

        result = parse(file_request)

        self.assertEqual(result, "txt content")

        mock_upload_llama_parse_pdf.assert_not_called()
        mock_get_llama_parse.assert_not_called()
        mock_save_file.assert_not_called()

    def test_parse_md(self, mock_save_file: MagicMock, mock_get_llama_parse: MagicMock, mock_upload_llama_parse_pdf: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.md", io.BytesIO(b"md content"), "text/plain"),
                "project_name": "test_project"
            }
        )

        file_request = FileRequest(func.HttpRequest(
            method="POST",
            url="/api/embedder",
            headers={"Content-Type": multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        ))

        result = parse(file_request)

        self.assertEqual(result, "md content")

        mock_upload_llama_parse_pdf.assert_not_called()
        mock_get_llama_parse.assert_not_called()
        mock_save_file.assert_not_called()

    def test_parse_csv(self, mock_save_file: MagicMock, mock_get_llama_parse: MagicMock, mock_upload_llama_parse_pdf: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.csv", io.BytesIO(b"csv content"), "text/plain"),
                "project_name": "test_project"
            }
        )

        file_request = FileRequest(func.HttpRequest(
            method="POST",
            url="/api/embedder",
            headers={"Content-Type": multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        ))

        result = parse(file_request)

        self.assertEqual(result, "csv content")

        mock_upload_llama_parse_pdf.assert_not_called()
        mock_get_llama_parse.assert_not_called()
        mock_save_file.assert_not_called()

    def test_parse_unsupported_extension(self, mock_save_file: MagicMock, mock_get_llama_parse: MagicMock, mock_upload_llama_parse_pdf: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.exe", io.BytesIO(b"exe content"), "application/octet-stream"),
                "project_name": "test_project"
            }
        )

        file_request = FileRequest(func.HttpRequest(
            method="POST",
            url="/api/embedder",
            headers={"Content-Type": multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        ))

        with self.assertRaises(Exception) as context:
            parse(file_request)

        self.assertEqual(str(context.exception), "Unsupported file extension")

        mock_upload_llama_parse_pdf.assert_not_called()
        mock_get_llama_parse.assert_not_called()
        mock_save_file.assert_not_called()

if __name__ == "__main__":
    unittest.main()