from file_embedder.file_request import FileRequest
from file_embedder.file_save.file_save import save_file

def filter_with_regex_and_save(content: str, file_request: FileRequest) -> str:
    filtered_content = content
    if file_request.get_remove_regex() is not None:
        filtered_content = file_request.get_remove_regex().sub("", content)
    
    save_file(
        content=filtered_content,
        file_path=file_request.get_file_path_text_file()
    )

    return filtered_content
