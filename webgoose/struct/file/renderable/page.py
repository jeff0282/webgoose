
import  cmarkgfm
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

    # CLASS ATTRS
    TEMPLATE_META_KEY = "template"
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

        # Set defaults for content and template 
        content = content if content else ""
        template = template if template else self.get_template_from_string(self.DEFAULT_TEMPLATE_STR)
        
        # set instance vars (cheers super)
        super().__init__(content=content, template=template, **render_args)
        self.metadata = meta if meta else dict()

        # put a copy of content under plain_content
        # content will be coverted to markup when `render()` is called
        self.context.add_fixed(plain_content=content)

    
    @property
    def plain_content(self) -> str:
        """
        The plain text version of this Page's content
        """
        return self.context['plain_content']


    @classmethod
    def from_file(cls, path: os.PathLike | str, **render_args: Any) -> Type['Page']:
        """
        Create a Page instance from a markdown + YAML frontmatter formatted file
        """

        # split and parse frontmatter and content 
        with open(path, "r", encoding='utf8') as f:
            meta, content = frontmatter.parse(f)

        # get template if provided in meta
        template = meta.get(cls.TEMPLATE_META_KEY, None)

        # create the thing :3
        return cls(content=content, meta=meta, template=template, **render_args)
    

    def render(self, **external_render_args: Any) -> str:
        self.content = cmarkgfm.github_flavored_markdown_to_html(self.content)
        return super().render(**external_render_args)
