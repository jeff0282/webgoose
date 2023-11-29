"""
webgoose.struct.file.file_like
"""


import  os

from    typing      import      Any
from    typing      import      Type
from    typing      import      TypeVar

from    pathvalidate    import      ValidationError
from    pathvalidate    import      validate_filepath

from    ..filelike      import      InvalidPathError
from    ..filelike      import      NotAnOrphanError
from    ..filelike      import      NotIndexableError


class FileLike():
    """
    
    """

    # Attachment Point
    # When a FileLike is attached to a parent, it's relative path (slug)
    # from that parent is set.
    #
    # The attach_point stores this information in a dict with 3 entries
    # - slug: The relative path from the parent to attach at
    # - is_index: Whether or not this instance is a Directory Index
    # - parent: A reference to the parent filelike instance
    AttachPoint = TypeVar("AttachPoint", dict[str, str | bool | Type['FileLike']])
    _attach_point: AttachPoint | None


    def __init__(self) -> None:
        """
        
        """
        self._attach_point = None


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.slug})"
    

    def __str__(self) -> str:
        return self.path
    

    def __eq__(self, cmp: Any) -> bool:
        return cmp is self
    

    def __hash__(self) -> int:
        return hash(self.slug)
    

    @property
    def indexable(self) -> bool:
        """
        Returns True if this file can be used as a Directory Index
        """
        return hasattr(self, "index_filename")
    

    @property
    def is_index(self) -> bool:
        """
        Returns True if this file is attached and is a Directory Index
        """
        if self.attach_point:
            return self.attach_point['is_index']
        
        return False
    

    @property
    def attach_point(self) -> AttachPoint | None:
        """
        A dictionary containing details on this instance's attachment to its
        parent

        If not attached, returns None
        """
        return self._attach_point
    

    def set_attach_point(self, 
                         *, 
                         slug: str, 
                         parent: Type['FileLike'], 
                         is_index: bool = False
                         ) -> None:
        """
        
        """

        # check if node is already attached
        if self.attach_point:
            raise NotAnOrphanError(f"Cannot set attachment point; '{self}' is already attached to '{self.parent}'")
        
        # if attempting to set as directory index, ensure that's possible
        if is_index:
            if not self.indexable:
                raise NotIndexableError(f"Cannot attach as a directory index; '{self}' is not indexable")
        
        # validate the string slug
        self.validate_slug(slug)

        # if all good, set up child-to-parent connection
        slug = os.path.normpath(slug)
        self._attach_point = dict(slug=slug, parent=parent, is_index=is_index)


    @property
    def slug(self) -> str:
        """

        """
        if self.attach_point:
            slug = self.attach_point["slug"]
            if not slug == os.curdir:
                return slug
        return ""
    

    @property
    def parent(self) -> Type['FileLike'] | None:
        """
        
        """
        if self.attach_point:
            return self.attach_point["parent"]
        return None


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
            i = self.filename.index(os.extsep, 1)
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
            i = self.filename.index(os.extsep, 1)
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

        # chop off first seperator, then split by sep'
        ext = self.ext[1:]
        return tuple(ext.split(os.extsep))


    @property
    def parts(self) -> tuple[Type['FileLike']]:
        """
        Returns a tuple of each parent node from this node,
        in order root-to-node
        """
        parts = []
        current_node = self
        while current_node:
            parts.append(current_node)
            current_node = current_node.parent

        return tuple(reversed(parts))


    @property
    def path(self) -> str:
        """
        Returns the full string path of a file object
        """

        # join together segments by their paths
        return os.sep.join(parts.slug for parts in self.parts if parts.slug)


    def validate_slug(self, slug: str):
        """
        Validate a file path slug
        """

        # check for os.pardir segments in slug
        if any(part for part in slug.split(os.sep) if part == os.pardir):
            raise InvalidPathError(f"Invalid Path: Paths must not contain parent dir references '{os.pardir}'")

        # See if path is well formed
        try:
            validate_filepath(slug)
        
        except ValidationError as e:
            raise InvalidPathError(f"Invalid Path: '{slug}' is not a valid path") from e
        
        # if path well formed, check if relative
        if os.path.isabs(slug):
            raise InvalidPathError(f"Invalid Path: '{slug}' path given must be relative, not absolute")