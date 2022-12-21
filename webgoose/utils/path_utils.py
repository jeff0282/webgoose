
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



def map_path(source_dir: str, dest_dir: str, source_path: str) -> Union[str,bool]:

    """
    Converts a File Path In One Directory to a Path Within The Destination Dir, Respecting Folder Structure Of SourceDir
    (i.e. strips off source_dir prefix from source_path, and sticks it on the end on the destination_dir)

    Returns 'False' If SourceDir is not within SourcePath
    """

    # Get Suffix Of Source Path, using Source Dir as Prefix, MAY RETURN FALSE
    rel_dest_path = strip_prefix(source_dir, source_path)

    # Strip Off First '/' If Present In rel_build_path To Avoid os.path.join() Treating 2nd Arg As An Absolute Path
    if rel_dest_path:

        dest_path = rel_dest_path[1:] if rel_dest_path[0] == "/" else rel_dest_path
        return os.path.join(dest_dir, dest_path)

    # If Source Dir is NOT a Prefix of Source Path, Return False 
    else:

        return False



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
    


def strip_prefix(prefix_dir: str, path: str) -> Union[str,bool]:

    """
    Strip A Common Prefix From A Path

    Returned path will ALWAYS be relative (no leading '/')

    Returns False if prefix_path is not in path
    """

    # Test Whether Prefix_Dir is a prefix of Path
    if os.path.commonprefix([prefix_dir, path]) != prefix_dir:
        return False

    # Given That Source_Dir is a prefix of Source_Path, Slice Of Length of Source_Dir from start
    suffix_path = path[len(prefix_dir):]

    # Strip Off First '/' If Present and Return
    return suffix_path[1:] if suffix_path[0] == '/' else suffix_path
