
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
        print(self.content)
        return re.sub(r"{&([^&]+)&}", self.applyMacro, self.content)


    def cleanSplitMacro(self, macro):
        listMacro = macro[2:-2].split(':')
        listMacro = list(map(lambda x: x.strip(), listMacro))
        
        # The REGEX That Finds Macros Forces Inclusion Of Inner Text
        # Thus Macro Command Can Be Assumed To Exist
        command = listMacro[0]
        arg = False
        if len(listMacro) > 1:
            arg = listMacro[1]
        
        return command, arg

    
    def applyMacro(self, macro):
        command, arg = self.cleanSplitMacro(macro.group(0))
        if command in self.MACROS.keys():
            return self.MACROS[command](arg) if arg else self.MACROS[command]()    
        
        return ""