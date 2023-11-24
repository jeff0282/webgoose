"""
webgoose

Welcome to the source code for Webgoose!

This place is a bit of a mess; it's my first proper programming related
project that isn't academic or for laughs.

This module outlines the objects available in Webgoose's Public API.

The below listed submodules typically contain __all__ which defines what 
should be available here
"""

# ---
# META
# > version
from    .version                import      __version__


# ---
# STRUCTS
# > site & components
from    .struct                 import      *

# > files & file groups
from    .struct.file            import      *
from    .struct.file_group      import      *

