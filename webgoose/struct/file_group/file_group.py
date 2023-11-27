
import  os

from    typing      import      Any
from    typing      import      Type
from    typing      import      Iterable
from    typing      import      Iterator
from    typing      import      Optional

from    wcmatch     import      glob

from    webgoose.struct.file     import      FileLike


class FileGroup:

    _files: set[Type[FileLike]]

    def __init__(self, initlist: Iterable[FileLike]) -> None:
        self._files = set(initlist)

    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self._files)})"


    def __len__(self) -> int:
        return len(self._files)


    def __bool__(self) -> bool:
        return bool(self._files)


    def __iter__(self) -> Iterator[Type[FileLike]]:
        for file in self._files:
            yield file


    def __contains__(self, cmp: Any) -> bool:
        if type(cmp) == str:
            return cmp.casefold() in self._files
        
        return cmp in self._files
    

    def get(self, slug: str, _default: Any | None = None) -> Type[FileLike] | Any | None:
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