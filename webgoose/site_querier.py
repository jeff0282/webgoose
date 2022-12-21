
from typing import Dict, List, Union

from webgoose import config
from webgoose import FileTraverser
from webgoose import PageQuerier
from webgoose import __version__
from webgoose.structs import WGSite
from webgoose.structs import WGFile
from webgoose.utils import file_utils


#
# CONSTANTS
#

# Extensions Seen As Page Source Files
PAGE_SOURCE_EXTS = [".md", ".html"]

# The Final Build Extension
PAGE_BUILD_EXT = ".html"


class SiteQuerier:

    def __init__(self, timestamp: float):

        """
        Initialise SiteQuerier Object With Timestamp (used as start-of-build time)

        Also Initialises Lists for Storing Types Of Files Found
        """

        self.__time = timestamp

        # EMPTY LISTS FOR TYPES OF FILES THAT MAY BE FOUND
        self.__all_files = []
        self.__static_files = []
        self.__pages = []
        self.__data_files = []




    def clear(self):

        """
        Resets All Lists To Default Values
        """

        self.__all_files = []
        self.__static_files = []
        self.__pages = []
        self.__data_files = []



    
    def get_site_info(self) -> WGSite:

        """
        Gathers All Site Information and Produces a WGSite Object
        """

        # Populate Instance File Lists With Files Found
        self.__get_all_files()

        # Return A Site Info Object Containing Everything
        return WGSite(self.__time, __version__, config, self.__all_files,
                    self.__pages, self.__static_files, self.__data_files)



    
    def __get_all_files(self):

        """
        Primary Method for Getting All Files From All Linked Directories
        """

        # Clear All Lists Before Starting, Just Incase
        self.clear()

        # Gather and Sort All Files In Source Directory
        self.__get_files_in_source_dir()

        # TODO: GET FILES FROM LINKED DIRS, DATA DIR, TEMPLATE DIR, ETC




    def __get_files_in_source_dir(self):

        """
        Wrapper Method For Getting All Types Of Files From The Source Directory
        """

        # Get All Files From Specified Source Directory
        file_paths = self.__get_files_in_dir(config['source_dir'])

        # Create WGFile Object For Each File, Additionally Separate and Handle Different File Types
        for path in file_paths:

            file_meta = file_utils.get_file_info(path)

            if file_meta['ext'] in PAGE_SOURCE_EXTS:

                self.__handle_page_file(file_meta)

            else:

                self.__handle_static_file(file_meta)
            


    def __get_data_files(self):

        """
        Retrieves Data Files From Data File Dir Specified In config.yaml
        """

        pass


    
    def __get_files_in_dir(self, path: str) -> List[str]:
        """
        A Convienience Wrapper For FileTraverser.find_files_rec()
        """

        traverser = FileTraverser(path)
        return traverser.find_files_rec()



    def __handle_page_file(self, file_meta: Dict[str, Union[str, float]]):

        """
        Handle Getting and Storing of Information For Files Identified As Page Source Files
        """

        # Get Build Path For File, Change Build Extension
        build_path = file_utils.map_path(config['source_dir'], config['build_dir'], file_meta['path'])

        # Extension May Already Be '.html', But This Doesn't Hurt :)
        build_path = file_utils.change_path_extension(build_path, PAGE_BUILD_EXT)

        # Add BuildPath and Optional BuildExt Values To FileMeta Dict
        file_meta['build_path'] = build_path
        file_meta['build_ext'] = PAGE_BUILD_EXT
    
        # Create WGFile Object
        file_obj = self.__make_wg_file(file_meta)

        # Add WGFile Object To Relevant Lists
        self.__all_files.append(file_obj)

        # Call on PageQuerier To Create A WGPage Object
        # !!!  THIS WILL NOT WORK  !!!
        page_querier = PageQuerier(file_obj)
        page_obj = page_querier.get_page_info()

        # Add WGPage Object To Relevant Lists
        self.__pages.append(page_obj)




    def __handle_static_file(self, file_meta: Dict[str, Union[str, float]]):

        """
        Handle Getting and Storing of Information For Files Identified As Static Files
        """

        # Get Build Path For File, Add To File_Meta Dict
        build_path = file_utils.map_path(config['source_dir'], config['build_dir'], file_meta['path'])
        file_meta['build_path'] = build_path

        # Create WGFile Object
        file_obj  = self.__make_wg_file(file_meta)

        # Add WGFile To All Files and Static Files Lists
        self.__all_files.append(file_obj)
        self.__static_files.append(file_obj)



    def __make_wg_file(self, file_meta: Dict[str, Union[str, float]]) -> WGFile:

        """
        Convienience Method For Creating A WGFile Object Using A File Metadata Dict
        """

        # Handle Optional Argument, build_ext
        if not "build_ext" in file_meta:
            file_meta['build_ext'] = None

        # Make and Return WGFile Object
        return WGFile(file_meta['path'], file_meta['build_path'], file_meta['basename'], 
                        file_meta['ext'], file_meta['build_ext'])
