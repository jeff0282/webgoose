
import os
import time

from typing import Dict, List

from webgoose import config
from webgoose import FileTraverser


class SiteGrabber:

    class SiteInfo:

        def __init__(self, time: float, site_config: Dict[str, str], source_files: List[str]):
            
            """
            Initialises A SiteInfo Object With Site Information Provided
            """

            self.__time = time
            self.__config = site_config
            self.__source_files = source_files



        @property
        def time(self) -> float:
            return self.__time

        @property
        def config(self) -> Dict[str, str]:
            return self.__config

        @property
        def source_files(self) -> List[str]:
            return self.__source_files



    
    def __init__(self):
        """ Nothing to be Set """
        pass



    def get_site_info(self) -> SiteInfo:

        """
        Gets All Site Info and Returns It As SiteInfo Object
        """

        time = time.time()
        source_files = self._get_all_source_files()

        return SiteInfo(self, time, config, source_files)



    def _get_all_source_files(self) -> List[str]:

        SOURCE_FILE_EXT = ".md"

        # Get All Markdown Files From Source Directory
        traverser = FileTraverser(config['build']['source-dir'])
        return traverser.find_files_rec(SOURCE_FILE_EXT)




