
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

    def __init__(self, initlist: Iterable[BaseFile]) -> None:
        self._files = set(initlist)

    
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