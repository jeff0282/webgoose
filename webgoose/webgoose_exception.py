
from typing import Optional


class WebgooseException(Exception):

    def __init__(self, name: Optional[str] = "WebgooseException", message: Optional[str] = "An Unknown Error Was Encountered During Runtime"):
        self.__name = name
        self.__message = message

    def __str__(self):
        return f"{self.__name} : {self.__message}"

    @property
    def name(self):
        return self.__name

    @property
    def message(self):
        return self.__message

    