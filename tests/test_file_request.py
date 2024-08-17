import unittest
import azure.functions as func
import io
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from file_embedder.file_request import FileRequest

class TestFileRequest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.txt", io.BytesIO(b"file content"), "text/plain"),
                "regex": "[a-z]",
                "project_name": "test_project"
            }
        )

        cls.req = func.HttpRequest(
            method="POST",
            url="/api/embedder",
            headers={"Content-Type": multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        )

    def test_get_filename(self):
        file_request = FileRequest(self.req)
        self.assertEqual(file_request.get_filename(), "test.txt")

    def test_get_content(self):
        file_request = FileRequest(self.req)
        self.assertEqual(file_request.get_content(), b"file content")

    def test_project_name(self):
        file_request = FileRequest(self.req)
        self.assertEqual(file_request.get_project_name(), "test_project")

    def test_get_regex(self):
        file_request = FileRequest(self.req)
        self.assertIsInstance(file_request.get_regex(), re.Pattern)
        self.assertEqual(file_request.get_regex().pattern, "[a-z]")
    
    def test_error_message(self):
        file_request = FileRequest(self.req)
        self.assertIsNone(file_request.error_message())

    def test_error_message_no_file(self):
        multipart_data = MultipartEncoder(
            fields={
                "project_name": "test_project",
                "regex": "[a-z]"
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

    def test_error_message_no_project_name(self):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.txt", io.BytesIO(b"file content"), "text/plain"),
                "regex": "[a-z]",
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

    def test_error_message_no_regex(self):
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

if __name__ == "__main__":
    unittest.main()
