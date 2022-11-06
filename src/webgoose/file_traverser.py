
import os
from typing import List, Optional, Tuple


class FileTraverserException(Exception):
    pass


# IMPROVE THIS !!!
class DirectoryNotFoundException(FileTraverserException):
    def __str__(self, directory: str):
        return f"The Directory Could Not Be Found"




class FileTraverser(object):


    def __init__(self, search_dir: str):
        self.search_dir = search_dir

    


    def find_recursive(self, extension: Optional[str] = "") -> Tuple[List[str], List[str]]:
        
        """ 
        Recursively Looks Through Directory and Subdirectories 
        for Folders and Files Matching The (Optional) Extention

        Time Complexity: bad :(
        """

        file_list = []
        dir_list = []

        if os.path.exists(self.search_dir):

            for (root, dirs, files) in os.walk(self.search_dir):

                partial_file_list = [os.path.join(root, x) for x in files if x.endswith(extension)]
                partial_dir_list = [os.path.join(root, x) for x in dirs]

                file_list.extend(partial_file_list)
                dir_list.extend(partial_dir_list)

        else:
            
            raise DirectoryNotFoundException()

        return dir_list, file_list





    def find(self, extension: Optional[str] = "") -> Tuple[List[str], List[str]]:

        """ 
        Finds All Files With Extension In The Directory Specified 
        When Instantiating PageTraverser Object 

        Time Complexity: O(2n) ??
        """

        if os.path.exists(self.search_dir):
            
            file_list = [x for x in os.listdir(self.search_dir) if os.path.isfile(x) and x.endswith(extension)]
            
            dir_list = [x for x in os.listdir(self.search_dir) if os.path.isdir(x)]

        else: 

            raise DirectoryNotFoundException()

        return dir_list, file_list
