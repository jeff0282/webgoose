
from typing import Dict, Optional, Union

from webgoose.structs import WGBaseFile



class WGFile(WGBaseFile):

    def __init__(self, file_meta: Dict[str, Union[str,float,None]]):

        """
        Initialise WGFile Object Using Dict Containing File Metadata

        Passes File_Meta Dict to 
        """

        # Initialises WGFile Object Using Meta Dict By Calling BaseFile Class
        super().__init__(file_meta)

        # HACK 
        # To make WGFile Attributes Immutable: 
        # - Set self.__attribute = self.attribute
        # - Make self.attributes a Property (OVERWRITING ORIGINAL ATTRIBUTES)
        # - Profit ???

        # Thanks to WGBaseFile, It Can Be Assumed These Attributes Exist:
        # .source_path, .build_path, .basename, .last_mod, .ext

        self.__source_path = self.source_path
        self.__build_path = self.build_path
        self.__basename = self.basename
        self.__last_mod = self.last_mod
        self.__ext = self.ext



    @property
    def _source_path(self) -> str:
        print("lol")
        return self.__source_path


    @property
    def _build_path(self) -> str:
        return self.__build_path


    @property
    def _basename(self) -> str:
        return self.__basename


    @property
    def _last_mod(self) -> float:
        return self.__last_mod


    def _ext(self) -> str:
        return self.__ext








                 

    
