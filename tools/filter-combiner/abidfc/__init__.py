__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .config import *
from .parser import (ParseError, parse_filterlist, parse_line)
from .combiner import ( IncludeError, MissingHeader, build_filterlist)
from .sources import ( FSSource, TopSource, WebSource)

"""
Exported members
----------------

Functions:
- parse_filterlist: Parse a filter list from an iterable of strings.
- parse_line      : Parse one line of a filter list.
- build_filterlist: Combine filter list fragments into a filter list.

Filter list fragment sources for filter list cobining:
- WebSource: loads fragments from the web.
- FSSource : loads fragments from a directory on the filesystem.
- TopSource: a specialized FSSource that represents current directory and should be
             used as the starting source of build_filterlist.

Exceptions that thrown by the functions in this module:
- ParseError   : thrown by the parser when invalid input is encountered.
- IncludeError : thrown by the combiner when an include instruction cannot be processed.
- MissingHeader: thrown by the combiner when the output doesn't start with a header.

See docstrings of module members for further information.

Notes
-----
`str` in function and method signatures always means a unicode string (Python3 meaning of
`str`).
"""

__all__ = [
    # Exceptions
    'ParseError',
    'IncludeError',
    'MissingHeader',
    # File sources
    'FSSource',
    'TopSource',
    'WebSource',
    # Functions
    'parse_filterlist',
    'parse_line',
    'build_filterlist',
]
