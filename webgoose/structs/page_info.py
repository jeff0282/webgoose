 

class PageInfo:

    """
    PageInfo - A Read-Only Struct For Storing Page Information Provided By PageGrabber
    """

    def __init__(self, source_path: str, build_path: str, last_mod_time: float,
                metadata: dict[str, str], template: str, content: str,):

        """
        Initialise PageInfo Object With All Page Information Provided
        """

        # Source File Info
        self.__source_path = source_path
        self.__build_path = build_path
        self.__last_mod = last_mod_time
        
        # Source File Contents
        self.__metadata = metadata
        self.__content = content

        # Info Derived From Source File
        self.__template = template



    @property
    def source_path(self) -> str:
        return self.__source_path

    @property
    def build_path(self) -> str:
        return self.__build_path

    @property
    def last_mod(self) -> float:
        return self.__last_mod

    @property
    def meta(self) -> dict[str, str]:
        return self.__metadata

    @property
    def raw_content(self) -> str:
        return self.__content

    @property
    def raw_template(self) -> str:
        return self.__template