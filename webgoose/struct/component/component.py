
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


class Component(BaseFile):
    """
    
    """

    _name: str
    _files: set[Type[File]]
    _subcomponents: set[Type['Component']]

    def __init__(self, name: str) -> None:
        """
        
        """

        self._validate_component_name(name)
        self._name = name
        self._files = set()
        self._subcomponents = set()

        super().__init__("")


    def __bool__(self) -> bool:
        return bool(self.files)
    

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
        # NAME IS RELIED UPON FOR HASHING
        #
        # NAME MUST NOT CHANGE ONCE COMPONENT IS ATTACHED
        return self.name


    @property
    def files(self) -> Type[FileGroup]:
        """
        This Component's files as a FileGroup
        """
        return FileGroup(self.files)


    @property
    def renderable(self) -> Type[RenderGroup]:
        """
        This component's renderable files as a RenderGroup
        """
        return RenderGroup((file for file in self.files if isinstance(file, Renderable)))
    

    @property
    def static(self) -> Type[FileGroup]:
        """
        This component's static files as a FileGroup
        """
        return FileGroup((file for file in self.files if isinstance(file, Renderable)))


    @property
    def subcomponents(self) -> Type[ComponentGroup]:
        """
        This Components Subcomponents as a ComponentGroup
        """
        return ComponentGroup(self._subcomponents)


    def add(self, 
            slug: str, 
            file_data_obj: Type[FileData]| os.PathLike | str, /) -> None:

        file_obj = self._create_file_from_data(slug, file_data_obj)
        super().add(file_obj)


    def get(self, slug: str, _default: Optional[Any] = None, /) -> Type[File] | Any | None:
        """
        Get a file by its slug (relative path)
        """

        return self.files.get(slug, _default)


    def attach_component(self, slug: str, subcomponent: Type['Component']) -> None:
        """
        Attach a subcomponent to this component
        """

        # perform duplicate check
        if subcomponent in self.subcomponents:
            raise ComponentExistsError(f"{self} already has component '{subcomponent}'")
        
        # attempt child-to-parent connection
        subcomponent._attach_to_parent(slug, self)

        self._subcomponents.add(subcomponent)


    def _attach_to_parent(self, slug: str, parent: Type['Component']) -> None:
        """
        Establish child-to-parent connect when attaching a subcomponent
        to a parent component

        Raises:
            - MalformedComponentNameError if slug is not valid
            - AlreadyAttachedError if this component is already attached to another parent
            (no such methods exist for cleanly detaching two components)
        """

        self._validate_slug(slug)
        if self.parent:
            raise AlreadyAttachedError(f"{self} is already attached to '{self.parent}'")
        

    def _create_file_from_data(self, 
                               slug: str, 
                               file_data_obj: Type[FileData]| os.PathLike | str, /) -> None:
        """
        Handle creation of file objects from file data

        Returns the appropriate file object dependent on file data type
        """

        # if file path given, assume static file, otherwise assume renderable file
        if isinstance(file_data_obj, os.PathLike) or type(file_data_obj) == str:
            file_obj = File(slug, Path(file_data_obj))

        else:
            file_obj = Renderable(slug, file_data_obj)

        return file_obj


    def _validate_component_name(self, name: str, /) -> None:
        """
        Validate a string name for use as a component name
        
        Raises MalformedComponentNameError on error
        """

        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$"):
            raise MalformedComponentNameError("""Invalid Component Name. Must only contain letters, 
                                              numbers & underscores, and be a valid Python attribute name""")


    def _validate_slug(self, slug: str) -> None:
        """
        Validate a file path slug
        """

        # Empty strings are valid slugs for components
        if slug == "":
            return None

        return super()._validate_slug(slug)