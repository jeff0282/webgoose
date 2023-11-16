
import  os

from    typing      import      Any
from    typing      import      Type
from    typing      import      Iterable
from    typing      import      Iterator
from    typing      import      Optional

from    wcmatch     import      glob

from    webgoose.struct     import      BaseFile


class FileGroup:

    _files: set[Type[BaseFile]]

    def __init__(self, 
                 initlist: Optional[Iterable[BaseFile]] = None) -> None:
        
        self._files = set()

        if initlist:
            for file in initlist:
                self.add(file)k

    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self._files)})"


    def __len__(self) -> int:
        return len(self._files)


    def __bool__(self) -> bool:
        return bool(self._files)


    def __iter__(self) -> Iterator[Type[BaseFile]]:
        for file in self._files:
            yield file


    def __contains__(self, cmp: Any) -> bool:
        return cmp in self._files


    def add(self, file_obj: Type[BaseFile]) -> None:
        if file_obj in self._files:
            raise FileExistsError(f"{self.__class__.__name__} already has a file at path '{file_obj.slug}'")
        
        self._files.add(file_obj)
    

    def get(self, slug: str, _default: Optional[Any] = None) -> Type[BaseFile] | Any | None:
        slug = os.path.normpath(slug)

        for file in self._files:
            if file.slug == slug:
                return file

        return _default
            

    def glob(self, pattern: str) -> Type['FileGroup']:
        matches = self.__class__()
        pattern = os.path.normpath(pattern)

        for file in self._files:
            if glob.globmatch(file.slug, pattern):
                matches.add(file)