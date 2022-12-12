
import re

from typing import Tuple



def split_filename(filename: str) -> Tuple[str, str]:

    """
    Splits A Filename Into Basename and Extension

    Returns Basename, Extension
    """

    # Set Defaults
    basename = ""
    extension = ""

    # Split Filename At Dot
    matches = re.match(r'([^\.]*)\.([^\.]*)', filename)

    # If No Dot Is Found In Regex Above, matches = None
    if matches:
        basename = matches.group(1)
        extension = matches.group(2)

    return basename, extension

