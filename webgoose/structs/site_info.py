
from typing import List

from webgoose.structs import WGFile


class SiteInfo:

    def __init__(self, time: float, site_config: Dict[str, str], all_files: List[WGFIle], 
                pages: List[WGFile], static_files: List[WGFile]):
        
        """
        Initialises A SiteInfo Object With Site Information Provided
        """

        # Timestamp Of Build Start and Config Dict
        self.__time = time
        self.__config = site_config

        # File Lists (Lists of WGFile Objects)
        self.__all_files = source_files
        self.__pages = pages
        self.__static_files = static_files



    @property
    def time(self) -> float:
        return self.__time

    @property
    def config(self) -> Dict[str, str]:
        return self.__config

    @property
    def all_files(self) -> List[WGFile]:
        return self.__all_files

    @property
    def pages(self) -> List[WGFile]:
        return self.__pages

    @property
    def static_files(self) -> List[WGFile]:
        return self.__static_files