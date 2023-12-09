
import  abc

from    typing      import      Any
from    typing      import      Type

from    pathvalidate    import      ValidationError
from    pathvalidate    import      validate_filename

from    .               import      FileLike
from    .               import      InvalidURIError
from    .               import      URI


class BaseFile(FileLike):
    """
    Base implementation of a file object; not for direct use

    Builds upon FileLike, providing additional validation for slugs 
    to ensure filename is valid.
    """
    

    def validate_slug(self, slug: Type[URI]) -> None:
        """
        """

        # check if filename is well-formed
        try:
            validate_filename(slug.basename)
        
        except ValidationError as e:
            raise InvalidURIError(f"Invalid Path: '{self.basename}' is not a valid filename") from e
        
        return super().validate_slug(slug)
    


class RenderableFile(BaseFile, metaclass=abc.ABCMeta):
    """
    Base Class for all Renderable File Classes

    All Renderable File classes should inherit from the class
    """
    
    @abc.abstractmethod
    def render(self, **render_args: Any) -> str | bytes:
        """
        Convert this file object into a string or bytes 
        to be output to disk
        """
        raise NotImplementedError()