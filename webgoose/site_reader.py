
import os

from typing import Optional, Union

from webgoose.structs import Site


#
# CONSTANTS
#

PAGE_SOURCE_EXTS = ['.md', '.html']


class SiteReader:


    def __init__(self, build_start_time: float) -> None:

        """
        Initialise SiteReader Object with Blank Fields For SiteInformation

        These Fields Will Be Populated by Class Methods

        Takes a Float Containing a Unix Timestamp of Start-of-Build
        """

        # Set Build-Time to passed Unix Timestamp
        self.__build_time = build_start_time

        # Set CWD Now, Just Incase
        self.__cwd = os.path.getcwd

        # Initialise Empty Lists For:
        # - File Information:
        self.__all_files = []
        self.__pages = []
        self.__static_files = []

        # - To Enable Checks To Be Performed:
        # (for URI conflict checks)
        self.__uris = []

        # TODO: AWAITING SUPPORT
        # self.__data_files = []



    def get_site(self) -> Site:

        """
        PRIMARY Public Method for Compiling All Site Information

        Returns a Site Object With All of this Information
        """

        pass



    def __clear_file_info(self) -> None:

        """
        Method to Clear All Site Lists For This Instance
        """

        self.__all_files = []
        self.__pages = []
        self.__static_files = []
        self.__uris = []



    def __get_files(self) -> None:

        """
        PRIMARY Method for Gathering All File Information from All Linked Dirs

        Dumps All Information Gatherer Into Instance Vars, Hence Private
        """

        # Clear All File Info, Just Incase
        self.__clear_file_info()

        # Get Pages Files From Source Directory
        self.__get_files_from_folder(config['source_dir'], True)

        # TODO:
        # - ADD SUPPORT FOR LINKING OTHER DIRECTORIES
        # - ADD SUPPORT FOR DATA FILES ???



    def __get_files_from_folder(self, search_dir: str, split_pages: Optional[Union[str,bool]] = False) -> None

        """
        Retrieves Files From Directory Specified

        OPTIONAL ARGS:
        - split_pages = True: SEPERATE AND HANDLE PAGES WITH SOURCE_PAGE EXTENSION
        """

        # Grab All Files From Given Directory (IGNORES HIDDEN FILES AND DIRS)
        traverser = FileTraverser(search_dir)
        page_paths = traverser.find_files_rec()

        # LOOK AT ME SEEM CLEVER WITH SOME "SEXY" FP STUFFS
        # (i'm shit at this, its not sexy at all !!)

        # Set Functions For Handling Of File Types (FileTraverser strips search_dir, so add as second arg)
        file_handler = lambda path: self.__handle_file(path, search_dir)

        # (if split_pages is True, set pages to be handlled seperately, otherwise, treat the same as a file)
        page_handler = lambda path: self.__handle_page(path, search_dir) if split_pages else file_handler

        # Loop through All Pages, Seperate As Necessary
        for path in page_paths:

            # Split Extension from Filename
            _, ext = os.path.splitext(path)

            # Seperate Files From Pages (see above lambda definitions, page and file handlers may be the same thing)
            # (If extension exists in valid source file extension list, treat as page)
            if ext.lower() in PAGE_SOURCE_EXTS:

                page_handler(path)

            else:

                file_handler(path)

            # Run Post Checks
            pass


        
        




    def __handle_file(self, path: str, source_dir: str) -> None:

        """
        Method For Handling Files Found

        Updates The File Lists (see __init__) Accordingly
        """

        # Create File Object Using FileFactory (responsible for getting information about file)
        file_factory = WGFileFactory(path, source_dir)
        file = file_factory.get_file()

        # Update Lists For File Information
        self.__all_files.append(file)
        self.__static_files.append(file)

        # Perform Post Checks
        # TODO
        # self.post_addition_checks(file)




    def __handle_page(self, path: str, source_dir: str) -> None:

        """
        Method For Handling Files Found

        Updates The File and Page Lists (see __init__) Accordingly
        """

        # Create Page Object Using PageFactory (responsible for getting information about page)
        page_factory = WGPageFactory(path, source_dir)

        # Get Page(s) (in some cases, single pages can be expanded out to multiple pages)
        # (the resulting 'pages' will be a list)
        pages = page_factory.get_pages()

        # Update Lists For Page Information
        self.__all_files.extend(pages)
        self.__pages.extend(pages)

        # Perform Post Checks
        # TODO
        # [self.post_addition_checks for page in pages]