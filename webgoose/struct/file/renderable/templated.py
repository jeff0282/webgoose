
import  os

from    typing      import      Any

from    jinja2      import      Environment
from    jinja2      import      FileSystemLoader
from    jinja2      import      Template

from    webgoose.struct         import      Context
from    webgoose.struct.file    import      PlainFile


class Templated(PlainFile):
    """
    
    """

    content: str

    # CLASS VARS
    DEFAULT_TEMPLATE_STR = "{% content %}" 
    JINJA2_ENV = Environment(
        loader = FileSystemLoader(os.curdir)
    )
    
    def __init__(self, 
                 *, 
                 content: str,
                 template: Template,
                 **render_args: Any) -> None:
        """
        Create a Templated File object

        Takes keyword args `content` (string or bytes) 
        and `template`, a jinja2.Template object
        
        Any additional keyword arguments are interpreted as 
        render args
        """
        
        super().__init__(content=content)
        self.template = template
        self.context.add(**render_args)


    def render(self, **render_args) -> str:
        """
        Render this file into a form that can be written to disk.
        Processes template using Jinja2 with this file's render args
        """
        
        # update context with any provided render args
        self.context.add(**render_args)

        # render the stuff
        self.template.render(self.context.to_dict())




