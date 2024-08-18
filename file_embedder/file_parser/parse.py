import os
from file_embedder.file_parser.get_llama_parse import get_llama_parse
from file_embedder.file_parser.upload_llama_parse import upload_llama_parse_pdf
from file_embedder.file_request import FileRequest
from file_embedder.file_save.file_save import save_file

def parse(file_request: FileRequest) -> str:
    extension = file_request.get_file_extension()
    if extension == "pdf":
        job_id = upload_llama_parse_pdf(
            file_content=file_request.get_content(),
            file_name=file_request.get_filename(),
            parsing_params=file_request.get_parsing_params()
        )
        content = get_llama_parse(job_id)

        file_name, _ = os.path.splitext(file_request.get_filename())
        file_path_with_txt = file_request.get_project_name() + "/" + file_name + ".txt"
        save_file(content=content, file_path=file_path_with_txt)

        return content
    elif extension in ("txt", "md", "csv"):
        content = file_request.get_content()
        return content.decode("utf-8")
    else:
        raise Exception("Unsupported file extension")
