
import  os

from    typing      import      Optional
from    typing      import      Type

from    dataclasses     import      dataclass
from    pathvalidate    import      validate_filepath
from    pathvalidate    import      ValidationError

from    webgoose.exceptions     import      _BaseWebgooseException



class InvalidPathError(_BaseWebgooseException):
    pass


@dataclass(frozen=True, kw_only=True)
class BaseFile:
    """
    The base implementation of a file object; not for direct use
    """

    slug: str
    data: Type[FileData]
    parent: Optional[Type['BaseFile']] = None

    def __post_init__(self) -> None:
        self._validate_slug(self.slug)


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.slug})"
    

    def __str__(self) -> str:
        return self.path
    

    @property
    def filename(self) -> str:
        """
        Returns the filename of a file object
        """
        return os.path.basename(self.slug)


    @property
    def dirname(self) -> str:
        """
        Returns the parent directory as a path
        """
        dirname, _ =  os.path.split(self.slug)
        return dirname


    @property
    def basename(self) -> str:
        """
        Returns the basename of a file object

        file.txt -> 'file'
        /this/is/a/file.txt -> 'file'
        """
        try:
            i = self.filename.rindex(os.extsep, 1)
            return self.filename[:i]

        except:
            return self.filename
    

    @property
    def ext(self) -> str:
        """
        Returns the extensions of a file, everything
        after the first dot (excluding leading dots)
        
        file.txt -> '.txt'
        .hidden.txt -> '.txt'
        archive.tar.gz -> '.tar.gz'
        """
        try:
            i = self.filename.rindex(os.extsep, 1)
            return self.filename[i:]

        except:
            return ""


    @property
    def exts(self) -> tuple[str]:
        """
        Returns a file object's extensions as a tuple of strings,
        excluding dots.

        archive.tar.gz -> ['tar', 'gz']
        """
        if not self.ext:
            return tuple()

        ext = self.ext[1:]
        return tuple(ext.split(os.extsep))


    @property
    def parts(self) -> tuple[Type['BaseFile']]:
        """
        Returns a tuple of each parent node from this node,
        in order root-to-node
        """
        parts = [self]

        current_node = self
        while current_node.parent:
            parts.append(current_node)
            current_node = current_node.parent

        return tuple(reversed(parts))


    @property
    def path(self) -> str:
        """
        Returns the full string path of a file object
        """
        os.sep.join(self.parts)


    @staticmethod
    def _validate_slug(path: str):
        """
        Validate a slug, checking that it's well-formed and is not absolute

        Platform independent (hopefully :3)
        """

        # See if path is well formed
        try:
            validate_filepath(path)
        
        except ValidationError as e:
            raise InvalidPathError(f"Invalid Path: '{path}' is not a valid path")
        
        # if path well formed, check if relative
        if os.path.isabs(path):
            raise InvalidPathError(f"Invalid Path: '{path}' path given must be relative, not absolute")