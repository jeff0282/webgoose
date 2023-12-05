
import  re
import  os

from    typing      import      Any
from    typing      import      Optional
from    typing      import      Type

from    ..filelike       import      FileLike
from    ..filelike       import      BaseFile
from    ..filelike       import      RenderableFile
from    ..filelike       import      StaticFile

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
        return bool(self.files) and bool(self.subcomponents)


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
    

    def group_meta(self, meta: str, *, include_missing: bool = False) -> dict[str, Any]:
        """
        Categorise all of this component's pages by a metadata tag

        Creates a dict with each of the values of a certain key found in the metadata for all files.

        Only metadata values that are hashable will be included (strings, integers, etc). 
        Non-hashables types are simply ignored.
        
        For iterable values, each item of the iterable will be used (provided the value is hashable)
        
        i.e:
          If we were to call component.group_meta("tags")

          A child page 'camping-post.html' with
          `tags: [outdoors, hiking, camping]`

          Would translate to:
        ```
        {
            'outdoors': [Page('camping-post.html']),
            'hiking': [Page('camping-post.html')],
            'camping': [Page('camping-post.html)] 
        }
        ```

          Any other pages with matching metadata attributes would be included in the lists
          with the respective keys.

        KW_Only Args:
            - `include_missing`: [Default = False] Adds a key `None` to the return dict for 
            all files either missing the given key, or where any of the key's values equals None
        """




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