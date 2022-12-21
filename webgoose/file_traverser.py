
import os
from typing import List, Optional


class FileTraverser(object):


    def __init__(self, search_dir: str):

        """
        Initialise FileTraverser Instance with a Directory Path
        """

        self.__search_dir = search_dir

    


    def find_files_rec(self) -> List[str]:
        
        """ 
        Recursively Looks Through Directory and Subdirectories For Files
        """

        file_list = []

        if os.path.exists(self.__search_dir):

            for (root, dirs, files) in os.walk(self.__search_dir):

                partial_file_list = [os.path.join(root, x) for x in files]
                file_list.extend(partial_file_list)

        else:
            
            raise FileNotFoundError(f"The Path '{self.search_dir}' Does Not Exist")

        return file_list





    def find_files(self) -> List[str]:

        """ 
        Finds All Files With Extension In The Directory Specified
        """

        if os.path.exists(self.__search_dir):
            
            file_list = [file for file in os.listdir(self.__search_dir) if os.path.isfile(os.path.join(self.__search_dir, file))]

        else: 

            raise FileNotFoundError(f"The Path '{self.search_dir}' Does Not Exist")

        return file_list