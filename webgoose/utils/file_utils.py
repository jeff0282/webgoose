
import os
import re

from typing import Dict, Tuple, Union





def get_file_info(path: str) -> Dict[str, Union[str, float]]:

    """
    Get Basic Metadata About A File
    """

    # Get Basename and Extension From Filename
    filename = os.path.basename(path)
    basename, ext = os.path.splitext(filename)

    # Get Last Modified Time Of File As Float Epoch Timestamp
    last_mod = os.path.getmtime(path)

    return {'path': path, 'basename': basename, 'ext': ext, 'last_mod': last_mod}



def map_path(source_dir: str, dest_dir: str, source_path: str) -> str:

    """
    Converts a File Path In One Directory to a Path Within The Destination Dir, Respecting Folder Structure Of SourceDir
    (i.e. strips off source_dir prefix from source_path, and sticks it on the end on the destination_dir)

    Returns 'False' If SourceDir is not within SourcePath
    """

    # Test Whether SourceDir is a prefix of SourcePath
    if os.path.commonprefix([source_dir, source_path]) != source_dir:
        return False

    # Replace Source Dir In Source Path With Dest Dir
    # Strip Source Dir From Source Path, Put Dest_Dir At Front
    rel_dest_path = re.sub(r"^"+source_dir, "", source_path)

    # Strip Off First '/' If Present In rel_build_path To Avoid os.path.join() Treating 2nd Arg As An Absolute Path
    dest_path = rel_dest_path[1:] if rel_dest_path[0] == "/" else rel_dest_path
    return os.path.join(dest_dir, dest_path)



def change_path_extension(path: str, new_ext: str) -> Union[str,bool]:

    """
    Change Extension of File on Path
    """

    # Add a '.' to the start of 'new_ext' if not present
    new_ext = '.' + new_ext if new_ext[0] != '.' else new_ext

    dir, filename = os.path.split(path)

    # Filename will be null if path ends with '/'    
    if filename == "":
        return False

    basename, ext = os.path.splitext(filename)

    return os.path.join(dir, basename + new_ext)
    