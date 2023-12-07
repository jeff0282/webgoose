"""
webgoose.struct.file.file_like
"""

import  os

from    typing      import      Any
from    typing      import      Type

from    .           import      InvalidURIError
from    .           import      NotAnOrphanError
from    .           import      NotIndexableError
from    .           import      URI


class FileLike():
    """
    NOTE: Due to the architecture of FileLikes, root nodes cannot
    have slugs as slugs are only set when attaching to a parent.
    """

    # Attachment Point
    # When a FileLike is attached to a parent, it's relative path (slug)
    # from that parent is set.
    #
    # The attach_point stores this information in a dict with 3 entries
    # - slug: A Slug instance storing the relative URI from the parent
    # - is_index: Whether or not this instance is a Directory Index
    # - parent: A reference to the parent filelike instance
    _attach_point: dict[str, Any] | None


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


    @property
    def is_indexable(self) -> bool:
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
    def is_attached(self) -> bool:
        """
        Returns True if this file has it's attachment point set, false otherwise
        """

        return bool(self.attach_point)
    

    @property
    def attach_point(self) -> dict[str, Any] | None:
        """
        A dictionary containing details on this instance's attachment to its
        parent

        If not attached, returns None
        """

        return self._attach_point
    

    def set_attach_point(self, 
                         *, 
                         slug_str: str, 
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
        
        # Create the Slug instance to store relative path to parent
        slug = URI(slug_str)
        self.validate_slug(slug)

        # If all good set attachment point
        self._attach_point = dict(slug=slug, parent=parent, is_index=is_index)


    @property
    def slug(self) -> Type[URI]:
        """
        This file's URI relative to it's parent as a Slug
        """

        if self.attach_point:
            return self.attach_point["slug"]
        
        # return an empty URI if not attached
        return URI("")
    

    @property
    def parent(self) -> Type['FileLike'] | None:
        """
        This file's parent. Returns None if not attached to a parent
        """

        if self.attach_point:
            return self.attach_point["parent"]
        
        return None


    @property
    def filename(self) -> str:
        """
        Returns the filename of a file
        """

        return self.slug.filename


    @property
    def basename(self) -> str:
        """
        Returns the basename of this file

        file.txt -> 'file'
        /this/is/a/file.txt -> 'file'
        """

        return self.slug.basename
    

    @property
    def ext(self) -> str:
        """
        Returns the extensions of a file, everything
        after the first dot (excluding leading dots)
        
        file.txt -> '.txt'
        .hidden.txt -> '.txt'
        archive.tar.gz -> '.tar.gz'
        """

        return self.slug.ext


    @property
    def exts(self) -> tuple[str]:
        """
        Returns a file object's extensions as a tuple of strings,
        excluding dots.

        archive.tar.gz -> ['tar', 'gz']
        """

        return self.slug.exts


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
    def dirname(self) -> str:
        """
        Returns this file's URI one level up

        If this file is a Directory Index, returns said directory
        """
        
        if self.is_index:
            return self.uri

        return self.uri.dirname


    @property
    def uri(self) -> Type[URI]:
        """
        Returns the URI of this file as a Slug

        Abbreviates filenames for Directory Indexes
        """

        # As FileLike paths are always relative to the root node
        # we need to add a POSIX seperator to the start

        # construct uri from parts slugs, skipping falsey values
        uri = URI.ext_sep + URI(*(part.slug for part in self.parts if part.slug))

        # trim filename if directory index
        if self.is_index:
            uri = uri.dirname

        return uri


    @property
    def rel_uri(self) -> Type[URI]:
        """
        Return the URI of this file as a string, relative to it's parent

        Abbreviates filenames for Directory Indexes
        """

        # if directory index, return dirname, otherwise return slug
        if self.is_index:
            return self.slug.dirname
        
        return self.slug

        
    def validate_slug(self, slug: Type[URI]):
        """
        Validate a file path slug
        """

        # if path well formed, check if relative
        if slug.is_absolute:
            raise InvalidURIError(f"Invalid Path '{slug}': Path given must be relative, not absolute")