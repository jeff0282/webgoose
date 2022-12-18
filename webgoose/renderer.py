
from typing import Any, Dict, Optional
from jinja2 import Environment, FileSystemLoader

from webgoose import config
from webgoose.structs import PageInfo
from webgoose.utils import render_utils


class Renderer:

    def __init__(self, page: PageInfo):

        """
        the
        """

        self.__page = page



    @property
    def page(self) -> PageInfo:
        return self.__page



    def render(self, args: Optional[Dict[Any, Any]] = {}) -> str:

        """
        the
        """

        # Apply Jinja2 Templating and Markup Page Content
        content = self.apply_jinja2(self.page.raw_content, args)
        content = render_utils.markdownify(content)

        # Add Content To Args Dict
        args['content'] = content

        # Apply Templating To Template        
        return self.apply_jinja2(self.page.raw_template, args)



    def apply_jinja2(self, input: str, args: Optional[Dict[Any, Any]] = {}) -> str:

        """
        Use Apply Jinja2 With Predefined Stuffs
        """

        # Setup Jinja2 Environment
        jinja_env = Environment(
            loader = FileSystemLoader(config["template_dir"])
        )

        # Create A Jinja2 Template From The Input String
        input = jinja_env.from_string(input)

        # Render Template Using Jinja2 Env and Dict of Arguments (variable_name: value)
        return input.render(args)