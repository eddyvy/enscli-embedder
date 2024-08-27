import unittest
from unittest.mock import patch, MagicMock
import azure.functions as func
from requests_toolbelt.multipart.encoder import MultipartEncoder
import io
from embed import service
from embed.file_request import FileRequest


class TestService(unittest.TestCase):

    @patch("embed.service.save_file")
    def test_execute_embedding(self, mock_save_file: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.txt", io.BytesIO(b"file content"), "text/plain"),
                "project_name": "test_project",
                "regex": "[a-z]"
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

        service.execute_embedding(file_request)

        mock_save_file.assert_called_once()

        _, kwargs = mock_save_file.call_args
        content = kwargs.get('content')
        file_path = kwargs.get('file_path')

        self.assertEqual(content, b"file content")
        self.assertEqual(file_path, "test_project/test.txt")


if __name__ == "__main__":
    unittest.main()
