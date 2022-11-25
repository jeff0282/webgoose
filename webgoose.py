
import time

from src.webgoose.config import config
from src.webgoose.file_traverser import FileTraverser
from src.webgoose.page_factory import PageFactory
from src.webgoose.page_renderer import PageRenderer

start = time.time()

# Get Files To Build
traverser = FileTraverser(config['build']['source-dir'])
_, pages_to_build = traverser.find_recursive(".md")


# Loop Through All Pages And Build 'em
for page_path in pages_to_build:

    page_factory = PageFactory(page_path)
    page = page_factory.get_page()

    renderer = PageRenderer(page)
    renderer.render()


end = time.time()
print(f"took {end - start} seconds")
