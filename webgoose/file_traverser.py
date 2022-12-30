
import os
from typing import List, Optional

from webgoose.utils import path_utils


class FileTraverser(object):

    """

    NOTE: WILL ALWAYS IGNORE HIDDEN FILES (i.e. FILES OR FOLDERS WITH DOT PREFIX)
    """


    def __init__(self, search_dir: str):

        """
        Initialise FileTraverser Instance with a Directory Path
        """

        self.__search_dir = search_dir

    


    def find_files_rec(self) -> List[str]:
        
        """ 
        Recursively Looks Through Directory and Subdirectories For Files
        """

        # Final Return List To Be Appended To
        file_list = []

        if os.path.exists(self.__search_dir):

            for (root, dirs, files) in os.walk(self.__search_dir, topdown=True):

                # For Each File Found, Join It With Root (with search_dir sliced off)
                partial_file_list = [self.__find_files_rec_helper(root, file) for file in files]

                # Impose Restriction On os.walk That Directories Searched Must Not Be Hidden
                # (topdown=True is REQUIRED for this to work)
                dirs[:] = [dir for dir in dirs if dir[0] != "."]

                # Add Files Found To The File List
                file_list.extend(partial_file_list)

        else:
            
            raise FileNotFoundError(f"The Path '{self.__search_dir}' Does Not Exist")

        return file_list


    
    def __find_files_rec_helper(self, root: str, file_path: str) -> str:

        """
        Helper Method for .find_files_rec() To Allow For Sexy-ish List Comprehension

        Strips the search_dir prefix from the root path, join it with the file path
        """

        # Combine Root and File_Path
        # (os.walk() returns the directory as part of 'root', we'll need to extract what we need)
        full_path = os.path.join(root, file_path)

        # strip_prefix() Always Removes Leading Slash From Path 
        # (A Path With Prefix Removed Must Be Relative)
        return path_utils.strip_prefix(self.__search_dir, full_path)



    def find_files(self) -> List[str]:

        """ 
        Finds All Files With Extension In The Directory Specified
        """

        if os.path.exists(self.__search_dir):
            
            file_list = [file for file in os.listdir(self.__search_dir) if os.path.isfile(os.path.join(self.__search_dir, file))]

        else: 

            raise FileNotFoundError(f"The Path '{self.search_dir}' Does Not Exist")

        return file_list