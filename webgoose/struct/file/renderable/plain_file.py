"""
Plain File Object

Basic Implementation of a Renderable File, that simply
contains string or bytes as content.

Rendering this type of file just outputs its content
"""

from    typing      import      Any

from    webgoose.struct         import      Context
from    webgoose.struct.file    import      RenderableFile


class PlainFile(RenderableFile):
    """
    The most basic implementation of a renderable file; containing
    nothing more than some content (string or bytes).

    Rendering this type of file just outputs its content
    unchanged.
    """

    content: str | bytes


    def __init__(self, 
                 *, 
                 content: str | bytes) -> None:
        """
        Create a plain file object, using a string or bytes
        as content
        """
        self.context = Context()
        self.content = content
        super().__init__()


    @property
    def content(self) -> str | bytes:
        """
        The content of this file
        """
        return self.context['content']
    

    @content.setter
    def content(self, content: str | bytes) -> None:
        """
        Set this files content
        """
        # 'content' is a fixed mapping, so we can't just overwrite it
        # Content may also not be set yet (initialisation), so we must check
        self.context.pop('content') if 'content' in self.context else None
        self.add_fixed(content=content)

        
    def render(self, **render_args: Any) -> str | bytes:
        """
        Render this file into a form that can be
        written to disk
        """
        return self.content