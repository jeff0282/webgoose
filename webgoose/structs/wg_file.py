
class WGFile:

    def __init__(self, file_path: str, basename: str, ext: str, last_mod: float):
        
        """
        Initialises Object Instance Will File Information

        Designed To Work In Conjunction With SiteQuerier
        """

        self.__path = file_path
        self.__basename = basename
        self.__ext = ext
        self.__last_mod = last_mod



    @property
    def path(self) -> str:
        return self.__path

    @property
    def basename(self) -> str:
        return self.__basename

    @property
    def ext(self) -> str:
        return self.__ext

    @property
    def last_mod(self) -> float:
        return self.__last_mod