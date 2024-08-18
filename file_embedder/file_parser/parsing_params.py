class ParsingParams:
    def __init__(self):
        self.__parsing_instruction = None
        self.__lang = None

    def set_param(self, key: str, value: str) -> None:
        if key == "parsing_instruction":
            self.__parsing_instruction = value
        elif key == "lang":
            self.__lang = value

    def get_parsing_instruction(self) -> str:
        return self.__parsing_instruction
    
    def get_lang(self) -> str:
        return self.__lang
