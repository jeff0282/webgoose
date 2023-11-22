"""
The base classes for renderable file objects 
"""

from    webgoose.struct.file     import      BaseFile

class RenderableFile(BaseFile):
    """
    Base Class for all Renderable File Objects
    """
    pass

class DataFile(RenderableFile):
    """
    Base Class for all Data File Objects

    Inherits from RenderableFile Base Class
    """
    pass