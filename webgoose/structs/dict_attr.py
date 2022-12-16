
from typing import Any, Dict

class DictAttr:

    """
    A Simple Struct to Enable The Auto-Magic Creation Of A Class Struct Using A Dictionary
    """

    def __init__(self, dict: Dict[Any, Any]):

        """
        For Each Dictionary Item, Create An Attribute With Name = Key and Value = Value

        For Duplicate Keys, They Are Simply Overwritten
        """

        for key, value in dict.items():
            
            # Check If Value == None (this is what Python-YAML spits out if value if empty)
            # (note: this IS unit tested)
            if value != None:
                setattr(self, key, value)