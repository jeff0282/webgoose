
import importlib
import re

macro = importlib.import_module("webgoose.macros")

class MacroProcessor(object):

    MACROS  =  {"last_modified":    macro.lastModified, 
                "version":          macro.version,
                "toc":              macro.tableOfContents,
                "random":           macro.random,
                "built_using":      macro.builtUsing,
                "docroot":          macro.docroot}


    def __init__(self):
        pass

    
    def processMacros(self, filePath, content):
        return re.sub(r"#?{@([^@\n\r]+)@}", lambda macro: self.applyMacro(filePath, content, macro), content)


    def formatMacro(self, macro):
        # Strip Delimeters '{@ @}' From Macro, Trim Resulting Whitespace
        macro = macro[2:-2].strip()
        
        command = re.match(r"^[^\s|\"]+", macro).group()
        args = re.findall(r"\"([^\"]+)\"", macro)        
        return command, args

    
    def applyMacro(self, filePath, content, macro):
        macro = macro.group()
        print(f"IDENTIFIED MACRO: {macro}")
        
        if macro[0] == "#":
            print("^ ignoring")
            return re.sub("@", "&#64;", macro)[1:]
        command, args = self.formatMacro(macro)
        if command in self.MACROS.keys():
            return self.MACROS[command](filePath, content, args)

        print(f"^ not a registered macro - removing from final markup")
        return ""