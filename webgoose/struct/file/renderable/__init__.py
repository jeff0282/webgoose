"""
webgoose.struct.file.renderable

Contains all renderable file classes
"""

__all__ = ['PlainFile', 'Templated', 'Page', 'Markdown']

# ---
# SET-UP BASE RENDERABLE CLASS
#
import  abc

from    typing      import      Any

from    webgoose.struct.file     import      BaseFile


class RenderableFile(BaseFile, metaclass=abc.ABCMeta):
    """
    Base Class for all Renderable File Classes

    All Renderable File classes should inherit from the class
    """
    
    @abc.abstractmethod
    def render(self, render_context: dict[str, Any]) -> str | bytes:
        """
        Convert this file object into a string or bytes 
        to be output to disk
        """
        raise NotImplementedError()
    

# ---
# MODULE IMPORTS
# > Renderable File Types
from    .plain_file         import      PlainFile
from    .templated          import      Templated
from    .page               import      Page
from    .markdown           import      Markdown