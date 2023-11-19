
import  re
import  os

from    typing      import      Any
from    typing      import      Iterable
from    typing      import      Optional
from    typing      import      Type

from    webgoose.struct         import      BaseFile
from    webgoose.struct         import      FileGroup



class ComponentExistsError(FileExistsError):
    pass


class MalformedComponentNameError(ValueError):
    pass


class BaseComponent(BaseFile):
    """
    
    """

    _files: set[Type[File]]
    _subcomponents: set[Type['BaseComponent']]

    def __init__(self, 
                 name: str,
                 slug: str, 
                 *,
                 parent: Optional[Type['BaseComponent']] = None) -> None:
        """
        
        """

        self._validate_component_name(name)
        # super init sets up child-to-parent connection
        super().__init__(slug, parent=parent)

        self._name = name
        self._files = set()
        self._file_group = FileGroup()
        self._subcomponents = ComponentGroup()

        # set up the parent-to-child connection
        # done last incase of error (ghost child ref in parent)
        if parent:
            parent._attach_subcomponent(self)


    def __bool__(self) -> bool:
        return self.files
    

    def __hash__(self) -> int:
        return hash(self.name)


    def __contains__(self, cmp: Any) -> bool:
        return cmp in self.files


    def __getattr__(self, key: str) -> Type['BaseComponent']:
        match = self.subcomponents.get_by_name(key, None)
        if match:
            return match

        raise AttributeError(f"{self} has no such attribute '{key}'")


    @property
    def name(self) -> str:
        """
        This Component's name.
        """
        self._name


    @property
    def files(self) -> Type[FileGroup]:
        """
        This Component's files as a FileGroup
        """
        return FileGroup(self._files)


    @property
    def subcomponents(self) -> Type[ComponentGroup]:
        """
        This Components Subcomponents as a ComponentGroup
        """
        return ComponentGroup(self._subcomponents)
    

    def _validate_component_name(self, name: str, /) -> None:
        """
        Validate a string name for use as a component name
        
        Raises MalformedComponentNameError on error
        """

        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$"):
            raise MalformedComponentNameError("""Invalid Component Name. Must only contain letters, 
                                              numbers & underscores, and be a valid Python attribute name""")


    def _attach_subcomponent(self, component: Type['BaseComponent']) -> None:
        """
        Attach a component as a child of this component.

        Only to be called in the child's constructor; constructor sets child-to-parent link
        """
        if component in self.subcomponents:
            raise ComponentExistsError(f"{self} already has a component with name '{component.name}'")
        
        # add subcomponent
        self._subcomponents.add(component)

        

    def add(self, file_obj: Type[File], /) -> None:
        """
        Add a file to this component
        """
        if file_obj in self.files:
            raise FileExistsError(f"{self} already has file at path '{file_obj.slug}'")

        # add file to component
        self._files.add(file_obj)


    def get(self, slug: str, _default: Optional[Any] = None, /) -> Type[File] | Any | None:
        """
        Get a file by its slug (relative path)
        """

        for item in self.files:
            if item.slug == slug:
                return item

        return _default


        



                    
        
    



    
    


