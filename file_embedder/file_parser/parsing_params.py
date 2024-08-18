import re

class ParsingParams:
    def __init__(self):
        self.__parsing_instruction = None
        self.__lang = None
        self.__regex = None

    def set_param(self, key: str, value: str) -> None:
        if key == "parsing_instruction":
            self.__parsing_instruction = value
        elif key == "lang":
            self.__lang = value
        elif key == "regex":
            self.__regex = re.compile(value)

    def get_parsing_instruction(self) -> str:
        return self.__parsing_instruction
    
    def get_lang(self) -> str:
        return self.__lang
    
    def get_regex(self) -> re.Pattern:
        return self.__regex
