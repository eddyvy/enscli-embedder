import logging
from azure.storage.blob import BlobServiceClient
import os

def save_file(content: bytes, file_path: str) -> None:
    logging.info(f"Saving {file_path}")

    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

    if not connection_string:
        raise EnvironmentError("AZURE_STORAGE_CONNECTION_STRING environment variable not set")
    
    if not container_name:
        raise EnvironmentError("AZURE_STORAGE_CONTAINER_NAME environment variable not set")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    if not container_client.exists():
        raise NameError(f"Container {container_name} does not exist")
    
    blob_client = container_client.get_blob_client(file_path)
    blob_client.upload_blob(content, overwrite=True)

    logging.info(f"Saved {file_path} succesfully")
