
import os
from typing import List, Optional

from webgoose import WebgooseException


class FileTraverserException(WebgooseException):
    def __init__(self, message: Optional[str] = "Error Opening Directory")
        super().__init__("FileTraverserException", message)




class FileTraverser(object):


    def __init__(self, search_dir: str):

        """
        Initialise FileTraverser Instance with a Directory Path
        """

        self.search_dir = search_dir

    


    def find_files_rec(self, extension: Optional[str] = "") -> List[str]:
        
        """ 
        Recursively Looks Through Directory and Subdirectories 
        for Files Matching The (Optional) Extention
        """

        file_list = []

        if os.path.exists(self.search_dir):

            for (root, dirs, files) in os.walk(self.search_dir):

                partial_file_list = [os.path.join(root, x) for x in files if x.endswith(extension)]
                file_list.extend(partial_file_list)

        else:
            
            raise DirectoryNotFoundException()

        return file_list





    def find_files(self, extension: Optional[str] = "") -> List[str]:

        """ 
        Finds All Files With Extension In The Directory Specified 
        When Instantiating FileTraverser Object 
        """

        if os.path.exists(self.search_dir):
            
            file_list = [x for x in os.listdir(self.search_dir) if os.path.isfile(os.path.join(self.search_dir, x)) and x.endswith(extension)]

        else: 

            raise DirectoryNotFoundException()

        return file_list