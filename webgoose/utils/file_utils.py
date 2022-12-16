
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

    # If Slashes In Filename, Strip Path To Only Base Filename
    last_slash_index = filename.rfind("/")
    if last_slash_index != -1:
        filename = filename[last_slash_index+1:]

    # Split Filename At Dot
    matches = re.match(r'([^\.]*)?(\.[^\.]*)?', filename)

    # If No Dot Is Found In Regex Above, matches = None
    if matches:
        basename = matches.group(1) if matches.group(1) else ""
        extension = matches.group(2) if matches.group(2) else ""

    return basename, extension

