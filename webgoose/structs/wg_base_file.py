
from typing import Dict, Optional, Union


#
# CONSTANTS
#

# Golden Dict for Checking File_Meta Dict
# [str, True] == Type Must Be 'str' and Is Required
# [str, False] == Type Must Be 'str' but This key:value Pair Is Not Required

ARGS = {

    'source_path': [str, True],
    'build_path': [str, True],
    'basename': [str, True],
    'last_mod': [float, True],
    'ext': [str, True]

}



class WGBaseFile:

    def __init__(self, file_meta: Dict[str, Union[str,float,None]]):

        """
        Initialise WGBaseFile Object Using Dict Containing File Metadata

        Checks Dict Passed Against 'Golden Dict', Checks Names and Types
        Discards Unknown Names, Raises Exception If Required Field Missing
        """

        # Loop Through Required Args, Check If Present and Set Attributes Appropriately
        for arg, arg_info in ARGS.items():

            # Check if Required Arg In Provided Dict
            if arg in file_meta:

                # Check If Type of Arg In Provided Dict Is Correct
                if type(file_meta[arg]) != arg_info[0]:

                    raise ValueError(f"Key '{arg}' In The Dict Passed To Type WGBaseFile Must Have A Value Of Type '{arg_info[0]}'")

            # If Required Arg Not Present In Dict, Raise Value Error If Value Required
            else:

                # If this Key:Value Pair Is Required, Throw Exception
                if arg_info[1] == True:

                    raise ValueError(f"Dict Passed To Type WGBaseFile Must Contain Key '{arg}")


        # If All Ok, Set Self.MetaDict
        self._meta_dict = file_meta






                 

    
