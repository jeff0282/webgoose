"""
webgoose.struct.file

Contains all files classes
"""

__all__ = ['StaticFile', 'Markdown', 'Page', 'YAML']


# > Exceptions
class InvalidPathError(ValueError):
    pass

class NotAnOrphanError(ValueError):
    pass


# > Base Classes
from    .file_like          import      FileLike
from    .base_file          import      BaseFile
from    .renderable.base    import      DataFile
from    .renderable.base    import      RenderableFile


# > Concrete Classes
from    .static_file            import      StaticFile
from    .renderable.markdown    import      Markdown
from    .renderable.page        import      Page
from    .renderable.yaml        import      YAML
