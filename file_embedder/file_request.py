import re
import azure.functions as func

from file_embedder.file_parser.parsing_params import ParsingParams

class FileRequest:
    __input_file = None
    __project_name: str = None
    __remove_regex: re.Pattern | None = None
    __parsing_params: ParsingParams

    def __init__(self, req: func.HttpRequest):
        for input_file in req.files.values():
            self.__input_file = input_file
            break

        self.__parsing_params = ParsingParams()
        
        for key, value in req.form.items():
            if key == "project_name":
                self.__project_name = value
            elif key == "remove_regex":
                self.__remove_regex = re.compile(value)
            else:
                self.__parsing_params.set_param(key, value)
            
    def error_message(self) -> str:
        if self.__input_file is None:
            return "No file uploaded"
        if self.__project_name is None:
            return "No project name provided"
        return None

    def get_filename(self) -> str:
        if self.__input_file is None:
            return ""
        return self.__input_file.filename
    
    def get_content(self) -> bytes:
        if self.__input_file is None:
            return None
        return self.__input_file.stream.read()
    
    def get_file_extension(self) -> str:
        if self.__input_file is None:
            return ""
        return self.__input_file.filename.split(".")[-1].lower()

    def get_project_name(self) -> str:
        return self.__project_name
    
    def get_remove_regex(self) -> re.Pattern | None:
        return self.__remove_regex

    def get_parsing_params(self) -> ParsingParams:
        return self.__parsing_params
