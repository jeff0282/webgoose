
import cmarkgfm


def markdownify(markdown: str) -> str:

    """
    Convert A Markdown String To HTML Using CMARK-GFM
    """

    return cmarkgfm.github_flavored_markdown_to_html(markdown)