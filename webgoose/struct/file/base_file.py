
import  os

from    typing      import      Any
from    typing      import      Optional
from    typing      import      Type

from    pathvalidate    import      validate_filepath
from    pathvalidate    import      ValidationError

from    webgoose.exceptions     import      BaseWebgooseException



class InvalidPathError(BaseWebgooseException):
    pass


class BaseFile:
    """
    The base implementation of a file object; not for direct use
    """

    _slug: str

    def __init__(self, 
                 slug: str,
                 *,
                 parent: Optional[Type['BaseFile']] = None) -> None:
    
        self._validate_slug(self.slug)
        self._slug = os.path.normpath(slug)
        self._parent = parent


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.slug})"
    

    def __str__(self) -> str:
        return self.path
    

    def __eq__(self, cmp: Any) -> bool:
        return cmp is self
    

    def __hash__(self) -> int:
        return hash(self.slug)
    

    @property
    def slug(self) -> str:
        return self._slug
    

    @property
    def parent(self) -> Optional[Type['BaseFile']]:
        return self._parent


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