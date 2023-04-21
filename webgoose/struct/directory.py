
import  yaml

from    pathlib     import      Path
from    typing      import      Any
from    typing      import      Dict
from    typing      import      List
from    typing      import      Union

from    webgoose.struct    import      Page


# CONSTANTS
# > filename/extension defaults
DIR_INFO_FNAME  = "dir.yaml"
PAGE_EXTS       = [".md"]


class Directory:


    def __init__(self, 
                path:       Path, 
                subdirs:    List[Path], 
                pages:      List[Page], 
                rec_pages:  List[Page],
                files:      List[Path],
                context:    Dict[str, Any],
                parent:     Union['Directory', None] = None):

        """
        Construct a Processed Directory Object to store information
        about a directory after it has been processed by the DirectoryProcessor.

        This class shouldn't really be used directly. It should instead be used through
        the DirectoryProcessor.
        """

        self.__path         = path
        self.__subdirs      = subdirs
        self.__pages        = pages
        self.__rec_pages    = rec_pages
        self.__files        = files
        self.__context      = context
        self.__parent       = parent


    # Read Only Properties
    # (yes, yes, I'm aware there are some mutable datatypes in here but idc)

    @property
    def path(self):
        return self.__path
    
    @property
    def subdirs(self):
        return self.__subdirs
    
    @property
    def pages(self):
        return self.__pages
    
    @property
    def rec_pages(self):
        return self.__rec_pages
    
    @property
    def files(self):
        return self.__files

    @property
    def context(self):
        return self.__context

    @property
    def parent(self):
        return self.__parent
    


    @classmethod
    def from_path(cls, 
                  path: Path, 
                  parent_dir: Union['Directory', None] = None, 
                  global_context: Union[Dict[str, Any], None] = None):

        # Check provided Path instance is a directory
        if not path.is_dir():
            raise NotADirectoryError()
        
        subdirs     = list()
        pages       = list()
        rec_pages   = list()
        files       = list()
        context     = dict()

        # Handle Auto-Population of Context & Rec Pages Lists
        # (items provided by parent directories)
        # Ensure global values (if supplied) can be overwritten by user-defined values
        if global_context:
            context.update(global_context)

        if parent_dir:
            rec_pages.append(parent_dir.rec_pages)
            context.update(parent_dir.context)


        for item in path.iterdir():

            if item.is_dir():
                subdirs.append(item)

            elif item.name == DIR_INFO_FNAME:
                context.update(cls.__get_yaml_file(item))

            elif item.suffix in PAGE_EXTS:
                pages.append(Page.from_path(item))

            # TODO: Rec Pages

            else:
                files.append(item)


        return cls(path, subdirs, pages, rec_pages, files, context, parent_dir)



    @staticmethod
    def __get_yaml_file(path: Path):

        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)



