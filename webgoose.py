
import time
from src.webgoose.file_traverser import FileTraverser
from src.webgoose.page_builder import PageBuilder

start = time.time()

traverser = FileTraverser("source")
builder = PageBuilder(traverser.get_all_md_files())
builder.build_all()

end = time.time()
print(f"took {end - start} seconds")



