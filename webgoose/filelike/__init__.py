"""
Webgoose - File Subpackage

The File-Like objects in this class aim to give a pre-render
representation of files of a Webgoose site
"""


# ---
# Exceptions
class InvalidURIError(ValueError):
    pass

class NotAnOrphanError(ValueError):
    pass

class NotIndexableError(ValueError):
    pass


# ---
# Module Imports
# > Supporting Classes
from    .slug               import      Slug
from    .render_context     import      RenderContext


# > Base Classes
#from    .file_like          import      FileLike
#from    .base               import      BaseFile
#from    .base               import      RenderableFile

    
# > Non-Renderable Built-in Types
#from    .static_file        import      StaticFile

# > Directory-Like
#from    .component          import      Component

# > Renderable Built-in Types
#from    .plain_file         import      PlainFile
#from    .templated          import      Templated
#from    .page               import      Page