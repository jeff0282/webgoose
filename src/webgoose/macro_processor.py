
import re
import subprocess

from typing import Optional, Union

import src.webgoose.macros as macros
from src.webgoose.webgoose_exception import WebgooseException
from src.webgoose.page_factory import PageFactory
from src.webgoose.config import config



class PreProcessorException(WebgooseException):

    def __init__(self, message="An Error Occured While Processing Macros"):
        super().__init__("PreProcessorException", message)




class PreProcessor():


    IGNORE_MACRO_PREFIX = "//"
    
    LOCAL_MACROS = config['macros']
    
    GLOBAL_MACROS = {

        "last_modified":    macros.last_modified, 
        "version":          macros.get_version,
        "toc":              macros.table_of_contents,
        "index":            macros.index,
        "docroot":          macros.docroot

    }


    def __init__(self, page: PageFactory.Page):

        # Initialise Instance Vars With Page Object, Placeholder Values
        self._page = page
        self.content = ""
        self.reference = ""




    # ==============
    # Public Methods
    # ==============

    def process_page(self) -> None:

        """ Method For Processing Macros On Any Given Content, With Optional Content To Reference """

        pass




    def process_macros(self, content: str, reference: Optional[Union[str, bool]] = False, **kwargs) -> str:

        """ 
        Public Method for Processing Macros In A Given String. Takes An Optional String For Reference and kwargs
        
        - The reference arg is used where macros need to read page content, this allows one to specify what content a macro can read.
          If no reference is provided, the content is used as both content and reference.

        - Kwargs are simply additional key, values pairs that can be interpreted as a macro, such as current block name
        """

        pass



    
    def _split_content_blocks(self, content: str) -> dict[str, str]:

        """ Splits blocks in page content into a dict with block name and block content """

        pass








































    """
    def process(self) -> str:

        # Pass Whole Page Content To Private Macro Processor Method
        processed_content = self.__apply_macros(self.manipulate)

        # Clean Up Processed Macros
        return self.clean_up(processed_content)




    def clean_up(self, manipulate: str) -> str:
        
        return manipulate.replace(self.IGNORE_MACRO_PREFIX+"{@", "{@")





    def unwrap_macro(self, macro: str) -> str:

        # Remove Macro Delimeters {@ ... @}, Strip Any Outer Whitespace
        # (removes first and last 2 characters from macro)
        macro = macro.group()[2:-2]

        # Return Unwrapped Macro, With Whitespace Stripped
        return macro.strip()
        


    
    def __apply_macros(self, manipulate: str) -> str:

        # Compile Regex Pattern (Purely For Sake Of Keeping Code Tidy)
        pattern = re.compile(r"(?<!"+self.IGNORE_MACRO_PREFIX+r"){@([^@\n\r]+)@}")

        # Replace Every Macro Found, Pass Each Match To __apply_single_macro()
        return re.sub(pattern, self.__apply_single_macro, manipulate)




    def __apply_single_macro(self, macro) -> str:

        # Unwrap Macro, Get Command As String
        macro_command = self.unwrap_macro(macro)

        # Set Default Return Value
        result = ""

         # Check If Macro Command Is Global Macro
        if macro_command in self.GLOBAL_MACROS:
            
            # Pass All Page Info, Full Page Content To Manipulate and Reference To Global Macro
            result = self.GLOBAL_MACROS[macro_command](self.page, self.manipulate, self.reference)

        # Check If Macro Command Is Local Macro
        elif macro_command in config['macros']:

            # Simply Return Macro Value (Local Macros Are {Key<string>, Value<string>} Pairs)
            result = config['macros'][macro_command]

        # Else, Assume Shell Command
        else:

            try:
                
                process = subprocess.run(macro_command, shell=True)

                if process.statuscode == 0:
                    result = str(process.stdout).strip()

            except Exception as e:

                print(f"Error While Processing Macro '{macro}' in '{page.source_path}':")
                print(e)
                print("Removing Macro From Page")
                


        return result
        """
