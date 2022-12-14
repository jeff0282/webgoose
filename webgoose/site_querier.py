
import os
import time

from typing import Dict, List, Tuple

from webgoose import config
from webgoose import FileTraverser
from webgoose.structs import SiteInfo
from webgoose.structs import WGFile
from webgoose.utils import file_utils


class SiteQuerier:
    
    def __init__(self, timestamp: float):

        """ Takes An Epoch Timestamp To Set As Build Time """

        self.time = timestamp 



    def get_site_info(self) -> SiteInfo:

        """
        Gets All Site Info and Returns It As SiteInfo Object
        """

        all_files = self.get_all_files()

        pages, static_files = self.seperate_pages_from_static_files(all_files)

        return SiteInfo(self.time, config, all_files, pages, static_files)



    def __get_all_files(self) -> List[str]:
        
        """
        Get All Files From Source Directory

        Returns A List Of Paths (Strings)
        """

        traverser = FileTraverser(config['build']['source-dir'])
        return traverser.find_files_rec()



    def get_all_files(self) -> List[WGFile]:

        """
        Gets All Files From Source Directory Using Private Method __get_all_files()

        Returns A List Of WGFiles With File Attributes
        """

        # Get List Of All File Paths In Source Directory
        file_paths = self.__get_all_files()

        # Initialise List For WGFile Objects
        files = []

        # !!! THIS COULD LIKELY BE IMPROVED !!!
        for file_path in file_paths:

            # Get Basename and Extension From Filename
            filename = os.path.basename(file_path)
            basename, ext = file_utils.split_filename(filename)

            # Get Last Modified Time Of File As Float Epoch Timestamp
            last_mod = os.path.getmtime(file_path)

            # Put File Info into a WGFile Object and Add To File List
            file = WGFile(file_path, basename, ext, last_mod)
            files.append(file)

        return files



    def seperate_pages_from_static_files(self, files_list: WGFile) -> Tuple[List[WGFile], List[WGFile]]:

        """
        Takes A List Of WGFile Objects, and Returns Two Sublist Containing Those That Are Source Pages, And Those That Aren't (Static Files)

        Anything That Isn't A Markdown File IS Assumed To Be A Static File.

        (It Just Checks If The File Extension Corresponds With a Markdown File :3)
        """

        PAGE_EXT = ".md"

        # Seperate WGFile Objects Into Pages, Static_Files Lists Depending On Whether or Not The File Extension Is PAGE_EXT
        pages, static_files = [file for file in files_list if file.ext.lower() == PAGE_EXT] , [file for file in files_list if file.ext.lower() != PAGE_EXT] 

        return pages, static_files

