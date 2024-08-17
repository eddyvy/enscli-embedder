import unittest
from unittest.mock import patch, MagicMock
from file_embedder.file_save.file_save import save_file

class TestFileSave(unittest.TestCase):

    @patch("file_embedder.file_save.file_save.BlobServiceClient")
    def test_save_file(self, mock_blob_service_client: MagicMock):
        with patch.dict("os.environ", {
            "AZURE_STORAGE_CONNECTION_STRING": "fake_connection_string",
            "AZURE_STORAGE_CONTAINER_NAME": "fake_container_name"
        }):
            mock_container_client = MagicMock()
            mock_blob_client = MagicMock()

            mock_blob_service_client.from_connection_string.return_value.get_container_client.return_value = mock_container_client
            mock_container_client.exists.return_value = True
            mock_container_client.get_blob_client.return_value = mock_blob_client

            save_file(b"file content", "test_project/test.txt")

            mock_blob_service_client.from_connection_string.assert_called_once_with("fake_connection_string")
            mock_container_client.get_blob_client.assert_called_once_with("test_project/test.txt")
            mock_blob_client.upload_blob.assert_called_once_with(b"file content", overwrite=True)

    @patch("file_embedder.file_save.file_save.BlobServiceClient")
    def test_save_file_no_connection_string(self, _: MagicMock):
        with patch.dict("os.environ", {
            "AZURE_STORAGE_CONNECTION_STRING": "",
            "AZURE_STORAGE_CONTAINER_NAME": "fake_container_name"
        }):
            with self.assertRaises(EnvironmentError) as context:
                save_file(b"file content", "test_project/test.txt")

            self.assertEqual(str(context.exception), "AZURE_STORAGE_CONNECTION_STRING environment variable not set")

    @patch("file_embedder.file_save.file_save.BlobServiceClient")
    def test_save_file_no_container_name(self, _: MagicMock):
        with patch.dict("os.environ", {
            "AZURE_STORAGE_CONNECTION_STRING": "fake_connection_string",
            "AZURE_STORAGE_CONTAINER_NAME": ""
        }):
            with self.assertRaises(EnvironmentError) as context:
                save_file(b"file content", "test_project/test.txt")

            self.assertEqual(str(context.exception), "AZURE_STORAGE_CONTAINER_NAME environment variable not set")

    @patch("file_embedder.file_save.file_save.BlobServiceClient")
    def test_save_file_container_not_exists(self, mock_blob_service_client: MagicMock):
        with patch.dict("os.environ", {
            "AZURE_STORAGE_CONNECTION_STRING": "fake_connection_string",
            "AZURE_STORAGE_CONTAINER_NAME": "fake_container_name"
        }):
            mock_container_client = MagicMock()

            mock_blob_service_client.from_connection_string.return_value.get_container_client.return_value = mock_container_client
            mock_container_client.exists.return_value = False

            with self.assertRaises(NameError) as context:
                save_file(b"file content", "test_project/test.txt")

            self.assertEqual(str(context.exception), "Container fake_container_name does not exist")

if __name__ == "__main__":
    unittest.main()
