import  abc
import  os

from    pathvalidate    import      ValidationError
from    pathvalidate    import      validate_filename

from    ..filelike        import      FileLike
from    ..filelike        import      InvalidPathError


class BaseFile(FileLike):
    """
    Base implementation of a file object; not for direct use

    Builds upon FileLike, providing additional validation for slugs 
    to ensure filename is valid.
    """
    

    def validate_slug(self, slug: str) -> None:
        """
        """

        # seperate filename for validation
        filename = os.path.basename(slug)

        # Prevent files from being called the current directory shorthand
        if filename == os.curdir:
            raise InvalidPathError(f"Filename cannot be '{os.curdir}'")

        # check if filename is well-formed
        try:
            validate_filename(filename)
        
        except ValidationError as e:
            raise InvalidPathError(f"Invalid Path: '{filename}' is not a valid filename") from e
        
        return super().validate_slug(slug)