import io
import unittest
import azure.functions as func
from unittest.mock import MagicMock, patch

from requests_toolbelt import MultipartEncoder
from file_embedder.file_request import FileRequest
from file_embedder.file_chunker.filter import filter_with_regex_and_save

@patch('file_embedder.file_chunker.filter.save_file')
class TestFilter(unittest.TestCase):

    def test_filter_with_regex_and_save_with_regex(self, mock_save_file: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.pdf", io.BytesIO(b"pdf content"), "application/json"),
                "project_name": "test_project",
                "remove_regex": r"^[1-9]\. ",
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

        content = """
1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua
"""
        filtered_content = filter_with_regex_and_save(content, file_request)

        expected_filtered_content = """
Lorem ipsum dolor sit amet
Consectetur adipiscing elit
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua
"""
        self.assertEqual(filtered_content, expected_filtered_content)

        mock_save_file.assert_called_once_with(content=expected_filtered_content, file_path="test_project/test.txt")

    def test_filter_with_regex_and_save_no_regex(self, mock_save_file):
        multipart_data = MultipartEncoder(
            fields={
                "file": ("test.md", io.BytesIO(b"md content"), "text/plain"),
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

        content = """
1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua
"""
        filtered_content = filter_with_regex_and_save(content, file_request)

        self.assertEqual(filtered_content, content)

        mock_save_file.assert_called_once_with(content=content, file_path="test_project/test.md")

if __name__ == '__main__':
    unittest.main()