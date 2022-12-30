
from typing import Dict, Optional, Union


#
# CONSTANTS
#

# Golden Dict for Checking File_Meta Dict
# [str, True] == Type Must Be 'str' and Is Required
# [str, False] == Type Must Be 'str' but This key:value Pair Is Not Required

ARGS = {

    'source_path': str,
    'basename': str,
    'last_mod': float,
    'ext': str

}



class WGBaseFile:

    def __init__(self, file_meta: Dict[str, Union[str,float,None]]):

        """
        Initialise WGBaseFile Object Using Dict Containing File Metadata

        ## THIS WILL THROW AN EXCEPTION IF THE FILE_META DICT ISN'T VALID ##
        """



        






                 

    
