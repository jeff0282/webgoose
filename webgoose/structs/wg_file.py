
from typing import Optional, Union

class WGFile:

    def __init__(self, source_path: str, build_path: str, basename: str, last_mod: float, ext: str, build_ext: Optional[Union[str, None]] = None):
        
        """
        Initialises Object Instance With File Information

        Designed To Work In Conjunction With SiteQuerier
        """

        self.__source_path = source_path
        self.__build_path = build_path
        self.__basename = basename
        self.__last_mod = last_mod
        self.__ext = ext
        self.__build_ext = build_ext



    @property
    def source_path(self) -> str:
        return self.__source_path

    @property
    def build_path(self) -> str:
        return self.__build_path

    @property
    def basename(self) -> str:
        return self.__basename

    @property
    def last_mod(self) -> float:
        return self.__last_mod

    @property
    def ext(self) -> str:
        return self.__ext

    @property
    def build_ext(self) -> Union[str,None]:
        return self.__build_ext