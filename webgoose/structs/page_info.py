
from webgoose.structs import WGFile


class PageInfo:

    """
    PageInfo - A Read-Only Struct For Storing Page Information Provided By PageQuerier
    """

    def __init__(self, source_path: str, build_path: str, basename: str, ext: str, 
                last_mod: float, metadata: dict[str, str], template: str, content: str):

        """
        Initialise PageInfo Object With All Page Information Provided
        """

        # WGFile Object


        # Source File Info
        self.__source_path = source_path
        self.__build_path = build_path
        self.__basename = basename
        self.__ext = ext
        self.__last_mod = last_mod_time
        
        # Source File Contents
        self.__metadata = metadata
        self.__raw_content = content

        # Info Derived From Source File
        self.__raw_template = template



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
    def ext(self) -> str:
        return self.__ext

    @property
    def last_mod(self) -> float:
        return self.__last_mod

    @property
    def meta(self) -> dict[str, str]:
        return self.__metadata

    @property
    def raw_content(self) -> str:
        return self.__raw_content

    @property
    def raw_template(self) -> str:
        return self.__raw_template