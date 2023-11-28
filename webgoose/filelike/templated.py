
import  os

from    typing      import      Any
from    typing      import      Type

from    jinja2      import      Environment
from    jinja2      import      FileSystemLoader
from    jinja2      import      Template
from    pathlib     import      Path

from    ..filelike    import      PlainFile


class Templated(PlainFile):
    """
    An Extension of PlainFile enabling templating through
    the Jinja2 Templating Engine

    Allows for additional render variables in templates by way
    of the `render_args` param and `context` instance var
    """

    content: str

    JINJA2_ENV = Environment(
        loader = FileSystemLoader(os.curdir)
    )
    
    def __init__(self, 
                 template: Template,
                 *, 
                 content: str,
                 **render_args: Any
                 ) -> None:
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


    @classmethod
    def from_file(cls,
                  template_path: os.PathLike | str,
                  *,
                  content: str,
                  **render_args
                  ) -> Type['Templated']:
        """
        Create a Templated object using a Jinja2 Template File
        """

        template = cls.get_template_from_path(template_path)
        return cls(content=content, template=template, **render_args)
    

    @classmethod
    def from_string(cls,
                    *,
                    content: str,
                    template_str: str,
                    **render_args
                    ) -> Type['Templated']:
        """
        Create a Templated instance using a string Jinja2 Template
        """

        template = cls.get_template_from_string(template_str)
        return cls(content=content, template=template, **render_args)
    

    @classmethod
    def get_template_from_path(cls, path: os.PathLike | str) -> Template:
        """
        Get a Template from a file

        Calls Jinja2 under-the-hood; allows loading template from pathcusing 
        Windows-style paths (`Jinja2.get_template()` only supports POXIX-Style paths)

        Raises TemplateNotFound error if not found
        """

        # Jinja2 uses POSIX-Style filepaths regardless of platform
        path = Path(path).as_posix()
        return cls.JINJA2_ENV.get_template(path)


    @classmethod
    def get_template_from_string(cls, string_template: str) -> Template:
        """
        Create a Template from a string

        Calls Jinja2 under-the-hood
        """

        return cls.JINJA2_ENV.from_string(string_template)


    def render(self, **external_render_args) -> str:
        """
        Render this file into a form that can be written to disk.
        
        Processes template using Jinja2 with this file's context and
        additional render args if provided
        """
        
        # update context with any provided render args
        self.context.add(**external_render_args)

        # render the stuff
        self.template.render(self.context.to_dict())


