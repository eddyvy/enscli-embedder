import re

class ParsingParams:
    def __init__(self):
        self.__template = None
        self.__lang = "es"
        self.__regex = None

    def set_param(self, key: str, value: str) -> None:
        if key == "template":
            self.__template = value
        elif key == "lang":
            self.__lang = value
        elif key == "regex":
            self.__regex = re.compile(value)

    def get_template(self) -> str:
        return self.__template
    
    def get_lang(self) -> str:
        return self.__lang
    
    def get_regex(self) -> re.Pattern:
        return self.__regex
