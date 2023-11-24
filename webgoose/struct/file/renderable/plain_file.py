"""
webgoose.struct.file.renderable.plain_file
"""

from    webgoose.struct.file    import      RenderableFile


class PlainFile(RenderableFile):
    """
    The most basic implementation of a renderable file; containing
    nothing more than some content (string or bytes).

    Rendering this type of file just outputs its content
    unchanged.
    """

    content: str | bytes


    def __init__(self, content: str | bytes) -> None:
        """
        Create a plain file object, using a string or bytes
        as content
        """
        self.content = content
        super().__init__()


    def render(self) -> str | bytes:
        """
        Render this file into a form that can be
        written to disk
        """
        return self.content