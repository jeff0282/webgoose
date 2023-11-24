
import  frontmatter
import  os

from    typing      import      Any
from    typing      import      Type

from    jinja2      import      Template

from    webgoose.struct.file    import      Templated


class Page(Templated):
    """
    
    """

    metadata: dict[str, Any]

    TEMPLATE_PATH_META_KEY = "template"
    DEFAULT_TEMPLATE_STR = r"{{content}}"

    def __init__(self,
                 *,
                 content: str | None = None,
                 meta: dict[str, Any] | None = None,
                 template: Template | None,
                 **render_args) -> None:
        """
        Create a Page File instance using some content, metadata, and a template
        """

        # set the stuff for superclass call
        content = content if content else ""
        if template: 
            template = template
        else:
            template = self.JINJA2_ENV.from_string(self.DEFAULT_TEMPLATE_STR)
        
        # set instance vars (cheers super)
        super().__init__(content=content, template=template, **render_args)
        self.metadata = meta if meta else dict()

        # put a copy of content under plain_content
        # content will be coverted to markup when `render()` is called
        self.context.add_fixed(plain_content=None)

    
    @property
    def plain_content(self) -> str:
        """
        The original version of this file's content,
        before markup conversion
        """
        return self.context['plain_content']


    @classmethod
    def from_file(cls, path: os.PathLike | str, **render_args: Any) -> Type['Page']:
        """
        Create a Page instance from a markdown + YAML frontmatter formatted file
        """

        if not os.path.exists(path):
            if not os.path.isfile():
                raise ValueError(f"The provided path '{str(path)}' is not a file")
        else:
            raise FileNotFoundError(f"The provided path '{str(path)} doesn't exist'")

        # split and parse frontmatter and content 
        with open(path, "r", encoding='utf8') as f:
            meta, content = frontmatter.parse(f)

        # get template if provided in meta, otherwise set default
        template = cls.JINJA2_ENV.from_string(cls.DEFAULT_TEMPLATE_STR)
        for k, v in meta.values():
            if k.casefold() == cls.TEMPLATE_PATH_META_KEY.casefold():
                template = cls.JINJA2_ENV.get_template(v)

        return cls(content=content, meta=meta, template=template, **render_args)
        

        

        


    def render

        
    


