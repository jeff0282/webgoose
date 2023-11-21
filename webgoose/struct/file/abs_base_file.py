
import  abc
import  os

from    pathvalidate    import      ValidationError
from    pathvalidate    import      validate_filename

from    webgoose.struct     import      AbstractFileLike
from    webgoose.struct     import      InvalidPathError


class AbstractBaseFile(AbstractFileLike):
    """
    """

    # ---
    # SUBCLASSES MUST IMPLEMENT THE BELOW
    # + those req'd from the super class

    @property
    @abc.abstractmethod
    def data(self) -> Type[FileData]:
        """
        """
        raise NotImplementedError()
    

    # ---
    # File Properties andOperations
    #

    def validate_slug(self, slug: str) -> None:
        """
        """

        # seperate filename for validation
        filename = os.path.basename

        # check if filename is well-formed
        try:
            validate_filename(filename)
        
        except ValidationError as e:
            raise InvalidPathError(f"Invalid Path: '{filename}' is not a valid filename") from e
        
        # Prevent files from being called the current directory shorthand
        if filename == os.curdir:
            raise InvalidPathError(f"Filename cannot be '{os.curdir}'")
        
        return super().validate_slug(slug)