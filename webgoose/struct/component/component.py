
import  re
import  os

from    typing      import      Any
from    typing      import      Optional
from    typing      import      Type

from    webgoose.exceptions     import      BaseWebgooseException
from    webgoose.struct         import      BaseFile
from    webgoose.struct         import      FileGroup



class ComponentExistsError(BaseWebgooseException):
    pass


class MalformedComponentNameError(BaseWebgooseException):
    pass


class Component(BaseFile):
    """
    
    """

    _files: list[Type[File]]
    _subcomponents: list[Type['Component']]

    # SUBGROUPS
    # the below subgroups are dynamically created and then cached by property getters
    # when the below attributes are set to None, it instructs the property to refresh the list
    # and set the respective attribute to the refreshed group
    _renderable_files: Optional[list[Type[Renderable]]]
    _static_files: Optional[list[Type[File]]]

    def __init__(self, 
                 name: str,
                 slug: str, 
                 *,
                 parent: Optional[Type['Component']] = None) -> None:
        """
        
        """

        self._validate_component_name(name)
        super().__init__(slug, parent=parent)

        self._name = name
        self._files = FileGroup()
        self._renderable_files = None
        self._static_files = None
        self._subcomponents = ComponentGroup()

        # set up the parent-to-child connection
        # done last incase of error (ghost child ref in parent)
        if parent:
            parent.subcomponents.add(self)


    def __contains__(self, cmp: Any) -> bool:
        return cmp in self.files


    def __getattr__(self, key: str) -> Type['Component']:
        match = self.subcomponents.get_by_name(key, None)
        if match:
            return match

        raise AttributeError(f"{self} has no such attribute '{key}'")


    @property
    def name(self) -> str:
        self._name


    @property
    def files(self) -> Type[FileGroup]:
        return self._files
    

    @property
    def 


    @property
    def subcomponents(self) -> Type[ComponentGroup]:
        return tuple(self._subcomponents)
    

    @staticmethod
    def _validate_component_name(self, name: str) -> None:
        """
        Validate a string name for use as a component name
        
        Raises MalformedComponentNameError on error
        """

        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$"):
            raise MalformedComponentNameError("""Invalid Component Name. Must only contain letters, 
                                                numbers & underscores, and be a valid Python attribute name""")


    def add(self,
            slug: str,
            file_data_obj: Type[FileData] | os.PathLike | str) -> None:
        """
        Add a file to this component

        If provided an os.PathLike or String object, assumes a path to a static file.
        Otherwise, file data object is assumed to be a Renderable
        """
        #TODO DIFFERENTIATE STATIC FROM RENDERABLE
        self._renderable_files = None
        self._static_files = None
        self.files.add(slug, file_data_obj)


    def get(self, slug: str, _default: Optional[Any] = None) -> Type[File] | Any | None:
        return self.get(slug, _default)


        



                    
        
    



    
    


