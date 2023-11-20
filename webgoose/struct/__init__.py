# webgoose.struct

# ---
# Exceptions
class InvalidPathError(ValueError):
    pass

class ComponentExistsError(FileExistsError):
    pass

class MalformedComponentNameError(ValueError):
    pass

class NotAnOrphanError(ValueError):
    pass

# ---
# File Structures
from    .file.abs_file_like         import      AbstractFileLike

# ---
# Components
from    .component.component        import      Component

# ---
# File Groups
from    .file_group     import      FileGroup

