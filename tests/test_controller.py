import unittest
from unittest.mock import patch, MagicMock
import azure.functions as func
from requests_toolbelt.multipart.encoder import MultipartEncoder
import io
from file_embedder import controller

class TestController(unittest.TestCase):

    @patch('file_embedder.controller.execute_embedding')
    def test_post_embedder(self, mock_execute_embedding: MagicMock):
        multipart_data = MultipartEncoder(
            fields={
                'file': ('test.txt', io.BytesIO(b'file content'), 'text/plain'),
                'project_name': 'test_project',
                'regex': '[a-z]'
            }
        )

        req = func.HttpRequest(
            method='POST',
            url='/api/embedder',
            headers={'Content-Type': multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        )

        resp = controller.post_embedder(req)

        self.assertIsInstance(resp, func.HttpResponse)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_body().decode(), 'success')

        mock_execute_embedding.assert_called_once()
        file_request = mock_execute_embedding.call_args[0][0]
        self.assertEqual(file_request.get_filename(), 'test.txt')
        self.assertEqual(file_request.get_content(), b'file content')
        self.assertEqual(file_request.get_regex().pattern, '[a-z]')

    def test_post_embedder_no_file(self):
        multipart_data = MultipartEncoder(
            fields={
                'project_name': 'test_project',
                'regex': '[a-z]'
            }
        )

        req = func.HttpRequest(
            method='POST',
            url='/api/embedder',
            headers={'Content-Type': multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        )

        resp = controller.post_embedder(req)

        self.assertIsInstance(resp, func.HttpResponse)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_body().decode(), 'No file uploaded')

    def test_post_embedder_no_project_name(self):
        multipart_data = MultipartEncoder(
            fields={
                'file': ('test.txt', io.BytesIO(b'file content'), 'text/plain'),
                'regex': '[a-z]'
            }
        )

        req = func.HttpRequest(
            method='POST',
            url='/api/embedder',
            headers={'Content-Type': multipart_data.content_type},
            params={},
            body=multipart_data.to_string()
        )

        resp = controller.post_embedder(req)

        self.assertIsInstance(resp, func.HttpResponse)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_body().decode(), 'No project name provided')

if __name__ == '__main__':
    unittest.main()
