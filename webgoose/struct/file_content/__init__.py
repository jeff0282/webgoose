"""
webgoose.struct.file_content

Defines the objects used for storing and manipulating data file contents
"""

# ---
# Necessary Pre-Amble
# (setting up base classes)
#
# These classes define the type of content and how they're handled
# File Content classes should inherit from one of these classes
#
# These base classes make use of abstract properties
# so that subclasses have standardised APIs, regardless
# of their underlying structure

import  abc

from    typing      import      Any

from    pathlib     import      Path


class BaseContent(metaclass=abc.ABCMeta):
    """
    Abstract Base Class for File Contents
    """
    pass


class StaticContent(BaseContent, metaclass=abc.ABCMeta):
    """
    Abstract Class for Static Files

    Defines a 'source' property that contains a Path object
    pointing to the source file
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{str(self.source)}')"
    
    @property
    @abc.abstractmethod
    def source(self) -> Path:
        raise NotImplementedError()


class RenderableContent(BaseContent, metaclass=abc.ABCMeta):
    """
    Abstract Class for transformable files contents

    Mandates the `content` property, and the `render()` method:
    - `content` returns the content of the file in question
    - `render()` transforms the content into a file-writiable form (str or bytes)
    """

    def __repr__(self) -> Any:
        return self.content
    
    @property
    @abc.abstractmethod
    def content(self) -> Any:
        raise NotImplementedError()

    @abc.abstractmethod
    def render() -> str | bytes:
        raise NotImplementedError()
    

class DataContent(RenderableContent, metaclass=abc.ABCMeta):
    """
    Abstract Class for Data Files (xml, json, etc)

    Adds nothing on-top of RenderableContent; purely exists
    for typing purposes
    """
    pass



# ---
# Module Imports
#

