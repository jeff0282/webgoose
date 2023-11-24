"""
webgoose.struct

Parent module for all the structures that make up Webgoose

This module only imports it's own stuff, doesn't mess with modules
in subfolders.

Submodules:
- File:         All file object representations
- File Group:   All file grouping classes
"""

__all__ = ['Context', 'Component']

# > Context
from    .context        import      Context

# > Components
from    .component      import      Component


