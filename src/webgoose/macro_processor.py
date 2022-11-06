
import re
from typing import Tuple

from bs4 import BeautifulSoup

from src.webgoose.config import config
from src.webgoose.macros import macros


class MacroProcessor():
    
    IGNORE_MACRO_PREFIX = "#"

    MACROS = {

        "last_modified":    macros.last_modified, 
        "version":          macros.version,
        "toc":              macros.table_of_contents,
        "index":            macros.index,
        "random":           macros.random,
        "time":             macros.time,
        "docroot":          macros.docroot

    }



    def __init__(self, file_path: str, content: str):
        
        self.file_path = file_path

        self.content = content




    def process(self) -> str:

        """
        Processes and Applies Macros To Page, Handles Ignored Macros and HTML Entity Bullshit :3
        """

        # Use BeautifulSoup Parser To Convert HTML Entities To Normal Text
        # (convert to string as it's a BeautifulSoup object by default)
        content = str(BeautifulSoup(self.content))
        
        # Process All Macros On Page
        processed_content = self.__apply_macros(content)

        # Macros Prefixed By A Hash Are To Be Ignored
        # Remove Hash Prefix From Ignored Macros
        processed_content = processed_content.replace(self.IGNORE_MACRO_PREFIX+"{@", "{@")

        return processed_content




    def __apply_macros(self, content: str) -> str:

        """
        Finds and Replaces Macros With Their Respective Output By Way Of Regex
        """

        # Compile Regex Pattern (Purely For Sake Of Keeping Code Tidy)
        pattern = re.compile(r"(?<!"+self.IGNORE_MACRO_PREFIX+"){@([^@\n\r]+)@}")

        return re.sub(pattern, lambda match: self.__apply_single_macro(self.content, match), content)






    def __apply_single_macro(self, content: str, macro: str) -> str:

        """
        Checks Validity Of and Gets The Output Of A Single Macro

        If Any Issue Occurs, It Just Spits Out The Empty String As The Macro Output
        """

        # Get Macro Name And Arguments As Key Value Dictionary From Macro String
        command, arg_dict = self.__parse_macro(macro.group())

        # Apply Macro If Present In The MACRO Dictionary, Otherwise Replace Macro With Empty String
        if command in self.MACROS:

            macro_result = self.MACROS[command](self.file_path, content, arg_dict)

            return macro_result
            

        # If Macro Not Found, Return Empty String
        return ""




    
    def __parse_macro(self, macro: str) -> Tuple[str, dict[str]]:

        """
        Parses Any Given Macro And Returns Its Name and Arguments

        Formats Macros So That:

            - {@ last_modified page=index.html format="%Y" @}

        Becomes:

            - Command: time
            - Argument: {'page': 'index.html', 'format': '%Y'}
        """

        # Remove Macro Delimeters {@ ... @}, Strip Any Outer Whitespace
        macro = macro[2:-2].strip()

        # Extract Macro Name
        command = re.match(r"^([^\s]+)", macro).group()
        
        # Extract Argument Keywords & Values From Macro
        arg_keywords = re.findall(r"(?<=\s)([^\s]+)(?=\=)", macro)

        arg_values = re.findall(r"(?<=\=\")([^\"]+)(?=\")", macro)

        # Create Dictionary From Keyword and Value Lists, If Arguments Were Provided
        # [NOTE] If List Lengths Are Mismatched, The Entire Entry (keyword: value) Will Be Ignored
        if arg_keywords and arg_values:
            
            arg_dict = {key:value for (key, value) in zip(arg_keywords, arg_values)}
            
            return command, arg_dict 

        return command, {}


        

