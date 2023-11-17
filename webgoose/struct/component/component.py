
import  os

from    pathlib     import      Path

from    webgoose.struct     import      BaseComponent
from    webgoose.struct     import      FileGroup

class Component(BaseComponent):

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


    def add(self, 
            slug: str, 
            file_data_obj: Type[FileData]| os.PathLike | str) -> None:

        file_obj = self._create_file_from_data(slug, file_data_obj)
        super().add(file_obj)


    def _create_file_from_data(self, 
                               slug: str, 
                               file_data_obj: Type[FileData]| os.PathLike | str) -> None:
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


        

