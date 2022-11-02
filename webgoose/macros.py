
def created(content, args):
    if args:
        return f"Created Macro Called - Value {args[0]}"
    
    return "Created Macro Called With No Value"


def lastModified(content, args):
    pass


def version(content, args):
    pass


def tableOfContents(content, args):
    pass


def random(content, args):
    if len(args) > 0:
        return ""
    return "myballs"


def builtUsing(content, args):
    pass