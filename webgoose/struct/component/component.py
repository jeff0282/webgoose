
import  re
import  os

from    typing      import      Any
from    typing      import      Optional
from    typing      import      Type

from    webgoose.struct         import      AbstractFileLike
from    webgoose.struct         import      FileGroup
from    webgoose.struct         import      NotAnOrphanError


class Component(AbstractFileLike):
    """
    
    """

    _name: str
    _attach_point: dict[str, Type['Component']] | None
    _files: set[Type[AbstractFileLike]]
    _subcomponents: set[Type['Component']]

    def __init__(self, name: str) -> None:
        """
        
        """

        # validate component name
        self._validate_component_name(name)
        
        # set instance vars
        self._name = name
        self._attach_point = None
        self._files = set()
        self._subcomponents = set()


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
    def attach_point(self) -> dict[str, Type['Component']] | None:
        """
        This Component's attach point
        """
        return self._attach_point
    

    @attach_point.setter
    def attach_point(self, 
                     attach_pnt_tuple: tuple[str, Type['Component']]) -> None:
        """
        
        """

        # Attempt to extract necessary info, string slug and parent component
        try:
            slug, parent = attach_pnt_tuple
        
        except ValueError as e:
            raise ValueError(f"Attach Point must be an interable in form '(str slug, parent component)'") from e

        # check if node is already attached
        if not self.attach_point:
            raise NotAnOrphanError(f"Cannot set attachment point, '{self}' is already attached to '{self.parent}'")
        
        # validate the string slug
        self.validate_slug(slug)

        # if all good, set up child-to-parent connection
        slug = os.path.normpath(slug)
        self._attach_point = dict(slug=slug, parent=parent)
    

    @property
    def parent(self) -> Type['Component'] | None:
        """
        This Component's parent
        """
        if self.attach_point:
            return self.attach_point["parent"]
        

    @property
    def slug(self) -> str | None:
        """
        This Component's slug
        """
        if self.attach_point:
            return self.attach_point["slug"]


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
        """
        
        """

        file_obj = self._create_file_from_data(slug, file_data_obj)
        super().add(file_obj)


    def get(self, slug: str, _default: Optional[Any] = None, /) -> Type[File] | Any | None:
        """
        Get a file by its slug (relative path)
        """

        return self.files.get(slug, _default)


    def attach_component(self, slug: str, subcomponent: Type['Component'], /) -> None:
        """
        Attach a subcomponent to this component
        """

        # perform duplicate check
        if subcomponent in self.subcomponents:
            raise ComponentExistsError(f"{self} already has component '{subcomponent}'")
        
        # attempt child-to-parent connection
        subcomponent._attach_to_parent(slug, self)

        # if no issues, add as child of this component
        self._subcomponents.add(subcomponent)
        

    def _create_file_from_data(self, 
                               slug: str, 
                               file_data_obj: Type[FileData]| os.PathLike | str, /) -> None:
        """
        Handle creation of file objects from file data

        Returns the appropriate file object dependent on file data type
        """

        # if file path given, assume static file, otherwise assume renderable file
        if isinstance(file_data_obj, os.PathLike) or type(file_data_obj) == str:
            file_obj = StaticFile(slug, Path(file_data_obj))

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