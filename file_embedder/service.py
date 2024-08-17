from file_embedder.file_request import FileRequest
from file_embedder.file_save.file_save import save_file

def execute_embedding(file_request: FileRequest) -> None:
    save_file(
        content=file_request.get_content(),
        file_path=file_request.get_project_name() + "/" + file_request.get_filename()
    )
