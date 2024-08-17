import azure.functions as func
import re

class FileRequest:
    __input_file = None
    __regex: re.Pattern | None = None
    __project_name: str = None

    def __init__(self, req: func.HttpRequest):
        for input_file in req.files.values():
            self.__input_file = input_file
            break
        
        for key, value in req.form.items():
            if key == "project_name":
                self.__project_name = value
            elif key == "regex":
                self.__regex = re.compile(value)
            
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

    def get_project_name(self) -> str:
        return self.__project_name

    def get_regex(self) -> re.Pattern | None:
        return self.__regex
