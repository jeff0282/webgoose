"""
Webgoose - File Subpackage

The File-Like objects in this class aim to give a pre-render
representation of files of a Webgoose site
"""


# ---
# Exceptions
class InvalidPathError(ValueError):
    pass

class NotAnOrphanError(ValueError):
    pass

class NotIndexableError(ValueError):
    pass

# ---
# Module Imports
# > Supporting Classes
from    .render_context     import      RenderContext

# > Base Classes
from    .file_like          import      FileLike
from    .base_file          import      BaseFile

# > Base Renderable Class
import  abc
from    typing      import      Any

class RenderableFile(BaseFile, metaclass=abc.ABCMeta):
    """
    Base Class for all Renderable File Classes

    All Renderable File classes should inherit from the class
    """
    
    @abc.abstractmethod
    def render(self, **render_args: Any) -> str | bytes:
        """
        Convert this file object into a string or bytes 
        to be output to disk
        """
        raise NotImplementedError()
    
# > Non-Renderable Built-in Types
from    .static_file        import      StaticFile

# > Directory-Like
from    .component          import      Component

# > Renderable Built-in Types
from    .plain_file         import      PlainFile
from    .templated          import      Templated
from    .page               import      Page