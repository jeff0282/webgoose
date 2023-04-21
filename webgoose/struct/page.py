
"""
page.py - Standard Page Object
"""

import  frontmatter

from    pathlib     import      Path
from    typing      import      Any
from    typing      import      Dict



class Page:

    def __init__(self, filename: str, meta: Dict[str, Any], body: str):
        
        self._filename  =   filename
        self._meta      =   meta
        self._body      =   body


    def __getattr__(self, name: str):
        return super.__getattribute__(self, name)


    @property
    def filename(self):
        return self._filename


    @property
    def meta(self):
        return self._meta


    @property
    def body(self):
        return self._body


    @property
    def template_path(self):

        """
        Get The Path To The Jinja2 Template From Page Metadata

        Path should be relative to templates folder. Default is None.
        """

        if "template" in self._meta.keys():
            return self._meta["template"]
        
        return None


    @classmethod
    def from_path(cls, path: Path):

        """
        Create A Page Object Using A pathlib.Path Object
        """

        with path.open("r", encoding="utf-8") as f:
            meta, body = frontmatter.parse(f.read())

        return cls(path.stem, meta, body)



    

    