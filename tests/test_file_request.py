import unittest
import azure.functions as func
import io
from unittest.mock import patch, MagicMock
from requests_toolbelt.multipart.encoder import MultipartEncoder
from file_embedder.file_request import FileRequest

@patch('file_embedder.file_request.ParsingParams')
class TestFileRequest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.txt", io.BytesIO(b"file content"), "text/plain"),
                "project_name": "test_project",
                "remove_regex": "[1-9]",
                "parsing_param_1": "value_1",
                "parsing_param_2": "value_2"
            }
        )

        cls.req = func.HttpRequest(
            method="POST",
            url="/api/embedder",
            headers={"Content-Type": multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        )

    def test_get_filename(self, _: MagicMock):
        file_request = FileRequest(self.req)
        self.assertEqual(file_request.get_filename(), "test.txt")

    def test_get_content(self, _: MagicMock):
        file_request = FileRequest(self.req)
        self.assertEqual(file_request.get_content(), b"file content")

    def test_project_name(self, _: MagicMock):
        file_request = FileRequest(self.req)
        self.assertEqual(file_request.get_project_name(), "test_project")

    def test_remove_regex(self, _: MagicMock):
        file_request = FileRequest(self.req)
        self.assertEqual(file_request.get_remove_regex().pattern, "[1-9]")
    
    def test_error_message(self, _: MagicMock):
        file_request = FileRequest(self.req)
        self.assertIsNone(file_request.error_message())

    def test_error_message_no_file(self, _: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                "project_name": "test_project",
                "parsing_param_1": "value_1",
                "parsing_param_2": "value_2"
            }
        )
                
        req = func.HttpRequest(
            method="POST",
            url="/api/embedder",
            headers={},
            params={},
            body=multipart_data.to_string()
        )

        file_request = FileRequest(req)
        self.assertEqual(file_request.error_message(), "No file uploaded")

    def test_error_message_no_project_name(self, _: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.txt", io.BytesIO(b"file content"), "text/plain"),
                "parsing_param_1": "value_1",
                "parsing_param_2": "value_2"
            }
        )

        req = func.HttpRequest(
            method="POST",
            url="/api/embedder",
            headers={"Content-Type": multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        )

        file_request = FileRequest(req)
        self.assertEqual(file_request.error_message(), "No project name provided")

    def test_error_message_no_parsing_params(self, _: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.txt", io.BytesIO(b"file content"), "text/plain"),
                "project_name": "test_project"
            }
        )

        req = func.HttpRequest(
            method="POST",
            url="/api/embedder",
            headers={"Content-Type": multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        )

        file_request = FileRequest(req)
        self.assertIsNone(file_request.error_message())

    def test_parsing_params_called_correctly(self, MockParsingParams: MagicMock):
        mock_parsing_params = MockParsingParams.return_value
        FileRequest(self.req)
        
        mock_parsing_params.set_param.assert_any_call("parsing_param_1", "value_1")
        mock_parsing_params.set_param.assert_any_call("parsing_param_2", "value_2")
        
        self.assertEqual(mock_parsing_params.set_param.call_count, 2)

    def test_get_file_extension(self, _: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.PDF", io.BytesIO(b"file content"), "application/pdf"),
                "project_name": "test_project",
                "parsing_param_1": "value_1",
                "parsing_param_2": "value_2"
            }
        )

        req = func.HttpRequest(
            method="POST",
            url="/api/embedder",
            headers={"Content-Type": multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        )

        file_request = FileRequest(req)
        self.assertEqual(file_request.get_file_extension(), "pdf")

if __name__ == "__main__":
    unittest.main()
