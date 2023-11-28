
import  re
import  os

from    typing      import      Any
from    typing      import      Optional
from    typing      import      Type

from    webgoose.filelike       import      FileLike
from    webgoose.filelike       import      BaseFile
from    webgoose.filelike       import      RenderableFile
from    webgoose.filelike       import      StaticFile

from    webgoose.group          import      ComponentGroup
from    webgoose.group          import      FileGroup
from    webgoose.group          import      RenderGroup    


class ComponentExistsError(FileExistsError):
    pass

class MalformedComponentNameError(ValueError):
    pass


class Component(FileLike):
    """
    
    """

    _name: str
    _files: set[Type[FileLike]]
    _subcomponents: set[Type['Component']]

    def __init__(self, name: str) -> None:
        """
        
        """

        # validate component name
        self._validate_component_name(name)
        
        # set instance vars
        self._name = name
        self._files = set()
        self._subcomponents = set()

        # complete initialise using superclass
        super().__init__()


    def __bool__(self) -> bool:
        return bool(self.files)
    

    def __hash__(self) -> int:
        return hash(self.name)


    def __contains__(self, cmp: Any) -> bool:
        return cmp in self.files


    def __getattr__(self, key: str) -> Type['Component']:
        match = self.subcomponents.get_by_name(key, None)
        if match:
            return match

        raise AttributeError(f"{self} has no such attribute '{key}'")


    @property
    def name(self) -> str:
        """
        This Component's name.
        """
        return self.name


    @property
    def files(self) -> Type[FileGroup]:
        """
        This Component's files as a FileGroup
        """
        return FileGroup(self._files)


    @property
    def renderable(self) -> Type[RenderGroup]:
        """
        This component's renderable files as a RenderGroup
        """
        return RenderGroup((file for file in self.files if isinstance(file, RenderableFile)))
    

    @property
    def static(self) -> Type[FileGroup]:
        """
        This component's static files as a FileGroup
        """
        return FileGroup((file for file in self.files if isinstance(file, StaticFile)))


    @property
    def subcomponents(self) -> Type[ComponentGroup]:
        """
        This Components Subcomponents as a ComponentGroup
        """
        return ComponentGroup(self._subcomponents)


    def add(self, slug: str, file: Type[BaseFile]| os.PathLike | str, /) -> None:
        """
        
        """

        if slug in self.files:
            raise FileExistsError(f"File with slug '{slug}' already exists in '{self}'")

        if isinstance(file, (os.PathLike, str)):
            file = StaticFile(file)

        file.attach_point = (slug, self)
        self._files.add(file)


    def get(self, slug: str, _default: Optional[Any] = None, /) -> Type[BaseFile] | Any | None:
        """
        Get a file by its slug (relative path)
        """

        return self.files.get(slug, _default)


    def attach_component(self, slug: str, subcomponent: Type['Component'], /) -> None:
        """
        Attach a subcomponent to this component
        """

        # components with duplicate slugs can exists
        # as components are hashed by their name
        if subcomponent in self.subcomponents:
            raise ComponentExistsError(f"{self} already has component '{subcomponent}'")
        
        subcomponent.attach_point = (slug, self)
        self._subcomponents.add(subcomponent)
        

    def _validate_component_name(self, name: str, /) -> None:
        """
        Validate a string name for use as a component name
        
        Raises MalformedComponentNameError on error
        """

        if not str.isidentifier(name):
            raise MalformedComponentNameError("Invalid Component Name: Component name must be a valid Python Identifier")