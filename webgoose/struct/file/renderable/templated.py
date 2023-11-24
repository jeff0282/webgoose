
import  os

from    typing      import      Any
from    typing      import      Optional

from    jinja2      import      Environment
from    jinja2      import      FileSystemLoader
from    jinja2      import      Template

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
                 template_str: Optional[str] = None,
                 template_path: Optional[os.PathLike | str] = None,
                 **render_args: Any) -> None:
        """
        Create a Templated File object

        Takes keyword args `content` (string or bytes) 
        and template params:
        - `template_str`: A Jinja2 Template as a string
        - `template_path`: A Path to a Jinja2 Template file
        
        If both provided, template_str takes priority.
        If none provided, the default template ``{% content %}`` is used
        
        Any additional keyword arguments are interpreted as 
        render args
        """

        # assert that two template values weren't provided
        if template_str and template_path:
            raise ValueError("Only ONE of either 'template_str' or 'template_path' should be provided, recieved both")
        
        # if template path provided, check that it exists
        if template_path:
            if os.path.exists(template_path):
                raise FileNotFoundError("Provided path to Template File doesn't exist")
        
        self._template_str = template_str
        self._template_path = template_path
        self.render_args = render_args

        super().__init__(content=content)


    @property
    def template(self) -> Template:
        """
        Returns a jinja2.Template object using the provided
        init params, or default if none provided
        """

        # check template str first, as it takes priority
        if self._template_str:
            return self.JINJA2_ENV.from_string(self._template_str)
        
        # otherwise, see if template path is set
        elif self._template_path:
            return self.JINJA2_ENV.get_template(self._template_path)
        
        # if none provided use the default 
        return self.JINJA2_ENV.from_string(self.DEFAULT_TEMPLATE_STR)
        

    def render(self, **external_render_args) -> str:
        """
        Render this file into a form that can be written to disk

        Processes Jinja2 template with content, render vars, and provided context
        """
        
        # local render args must take priority over external
        render_ctx = external_render_args + self.render_args
        return self.template.render(render_ctx)




