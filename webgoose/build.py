
import  time
import  os
import  yaml

from    pathlib     import      Path
from    typing      import      Any
from    typing      import      Dict
from    typing      import      Tuple

from    webgoose.render    import      PageRenderer
from    webgoose.struct    import      Directory
from    webgoose.struct    import      Page


# Constants
# [a lot of this will be moved to a config file + default values]

# > directory constants
TEMPLATES_DIR   = Path(".template/")
SOURCE_DIR      = Path(".src/")
BUILD_DIR       = Path("./")


# > filename/extension constants
PAGE_BUILD_EXT  = ".html"


class SiteBuilder:

    def __init__(self):
        
        """
        Construct a SiteBuilder Object for building a site.

        Automatically creates a PageRenderer instance and 
        loads default & config values.
        """

        self.renderer = PageRenderer(TEMPLATES_DIR)

        self.globals = {'build_time': time.time(),
                        'site_dir':   os.getcwd(),
                        'source_dir': SOURCE_DIR, 
                        'build_dir':  BUILD_DIR
        }


        

    def build(self):
        
        def rec_helper(path: Path, parent_dir: Directory, global_context: Dict[str, Any] = None):

            print(f"going through {path}")

            proccd_dir = Directory.from_path(path, global_context)
            self.__export_dir(proccd_dir)

            for subdir in proccd_dir.subdirs:
                rec_helper(subdir, proccd_dir)

        # Start Recursive Traversal of Source Folder
        # Include Global Values
        rec_helper(SOURCE_DIR, self.globals)



    def __export_dir(self, dir: Directory):

        # Convert source path to build path
        dir_build_path = BUILD_DIR.joinpath(dir.path.relative_to(SOURCE_DIR))
        
        # Make build dir for this directory
        dir_build_path.mkdir(parents=True, exist_ok=True)

        for page in dir.pages:
            
            rendered_page = self.renderer.render(page, dir.context)

            page_build_path = dir_build_path.joinpath(page.filename)

            page_build_path = page_build_path.with_suffix(PAGE_BUILD_EXT)

            with page_build_path.open("w+", encoding="utf-8") as f:
                print("writing")
                f.write(rendered_page)

