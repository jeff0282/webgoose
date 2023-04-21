
import  cmarkgfm

from    jinja2     import       Environment
from    jinja2     import       FileSystemLoader
from    pathlib    import       Path

from    typing     import       Any
from    typing     import       Dict

from    webgoose.struct     import      Page


class PageRenderer:


    def __init__(self, template_dir: Path):

        """
        Create A PageRenderer Object With Jinja2 Environment

        This should be used for as many pages as you wish!
        """
        
        self.jinja2_env  = Environment(
                            loader = FileSystemLoader(template_dir)
        )




    def render(self, page: Page, context: Dict[str, Any]):
        
        """
        Render A Page Object With A Given Context

        Process:
        - Render Content with Context
        - Convert Content Markdown to HTML
        - Render Template with Context (inclu. Content) & Return
        """

        # Render Content (body)
        content = self.jinja2_env.from_string(page.body).render(context)
        content = cmarkgfm.github_flavored_markdown_to_html(content)

        # Render Template With Content, Return When Done
        context['content'] = content
        print(context)
        return self.jinja2_env.get_template(page.template_path).render(context)