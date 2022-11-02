
import importlib, re
macro = importlib.import_module("webgoose.macros")

class MacroProcessor(object):

    MACROS  =  {"created":          macro.created, 
                "last_modified":    macro.lastModified, 
                "version":          macro.version,
                "toc":              macro.tableOfContents,
                "random":           macro.random,
                "built_using":      macro.builtUsing}


    def __init__(self, content):
        self.content = content

    
    def processMacros(self):
        return re.sub(r"{@([^@]+)@}", self.applyMacro, self.content)


    def splitMacro(self, macro):
        # Strip Delimeters '{@ @}' From Macro, Trim Resulting Whitespace
        macro = macro[2:-2].strip()
        
        command = re.match(r"^[^\s|\"]+", macro).group()
        args = re.findall(r"\"([^\"]+)\"", macro)        
        return command, args

    
    def applyMacro(self, macro):
        command, args = self.splitMacro(macro.group(0))
        if command in self.MACROS.keys():
            result = self.MACROS[command](self.content, args)
            return result
        
        return ""