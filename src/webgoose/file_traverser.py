
import os
from typing import List
from src.webgoose.config import config


class FileTraverserException(Exception):
    pass


class SourceDirectoryNotFoundException(FileTraverserException):
    def __str__(self):
        return "The Source Directory Could Not Be Found"



class FileTraverser(object):

    def __init__(self, searchDir: str):
        self.searchDir = searchDir

    


    def get_all_md_files(self) -> List[str]:
        
        """ Finds All Markdown Files In The Directory Specified When Instantiating PageTraverser Object """

        pathList = []

        if os.path.exists(self.searchDir):
            for (root, dirs, files) in os.walk(self.searchDir):
                partialList = [os.path.join(root, x) for x in files if self.is_markdown_file(x)]
                pathList.extend(partialList)
        else:
            raise SourceDirectoryNotFoundException()

        return pathList


    

    def is_markdown_file(self, filePath: str) -> bool:

        """ Simply Checks Is A File Is A Markdown File By Seeing If The Path Ends With '.md' (could be extended) """

        return filePath.endswith(".md")