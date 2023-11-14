
import  os

from    typing      import      Optional
from    typing      import      Type

from    pathvalidate    import      validate_filepath
from    pathvalidate    import      ValidationError

from    webgoose.exceptions             import      _BaseWebgooseException
from    webgoose.struct                 import      Component
from    webgoose.struct.file_group      import      _RenderSubgroup
from    webgoose.struct.file_group      import      _StaticSubgroup



class InvalidPathError(_BaseWebgooseException):
    pass


class FileGroup:

    _parent_component: Type[Component]
    _renderable: Type[_RenderSubgroup]
    _static: Type[_StaticSubgroup]


    def __init__(self, parent_component: Optional[Type[Component]] = None) -> None:
        
        self._parent_component = parent_component
        self._renderable = _RenderSubgroup(parent_group=self)
        self._static = _StaticSubgroup(parent_group=self)

    
    @property
    def static(self) -> Type[_StaticSubgroup]:
        return self._static
    

    @property
    def renderable(self) -> Type[_RenderSubgroup]:
        return self._renderable



    def add(self, renderable: Type[Renderable], rel_build_path: str) -> None:
        """
        Add a Renderable object to this file grouping

        Takes a Renderable object and a relative string path as build location

        Throws InvalidPathError if path provided is malformed or absolute
        """

        self._validate_build_path(rel_build_path)
        self.renderable.append(renderable)



    def add_static(self, static_file: os.Pathlike | Type[StaticFile], rel_build_path: str) -> None:
        """
        Add a static file to this file grouping

        Takes an os.PathLike object and a relative string path as build location

        Throws InvalidPathError if path provided is malformed or absolute
        """

        self._validate_rel_path(rel_build_path)
        self.static.append(static_file)
