
import time

from src.webgoose.file_traverser import FileTraverser
from src.webgoose.page_builder import PageBuilder

start = time.time()

traverser = FileTraverser("source")

_, pages_to_build = traverser.find_recursive(".md")

builder = PageBuilder(pages_to_build)

builder.build_all()

end = time.time()
print(f"took {end - start} seconds")



