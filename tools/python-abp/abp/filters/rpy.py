"""
Functions for integrating with rPython.

see: https://cran.r-project.org/web/packages/rPython/index.html
"""

from abp.filters import parse_line

__all__ = ['line2dict']


def line2dict(text, mode='body'):
    """Convert a filterlist line to a dictionary.

    All strings in the output dictionary will be UTF8 byte strings. This is
    necessary to prevent unicode encoding errors in rPython conversion layer.

    Parameters
    ----------
    text: str
        The filter text we want to parse
    mode: str
        Parsing mode (see `abp.filters.parser.parse_line`).

    Returns
    -------
    dict
        With the parsing results and all strings converted to utf8 byte
        strings.

    """
    return parse_line(text, mode).to_dict()


def lines2dicts(string_list, mode='body'):
    """Convert a list of filterlist strings to a dictionary.

    All strings in the output dictionary will be UTF8 byte strings. This is
    necessary to prevent unicode encoding errors in rPython conversion layer.

    Parameters
    ----------
    string_list: iterable of str
        Each string in the list can be an empty line, include instruction, or
        filter. If the mode is 'start', headers and metadata can also be
        parsed.
    mode: str
        Parsing mode (see `abp.filters.parser.parse_line`).

    Returns
    -------
    list of dict
        With the parsing results and all strings converted to utf8 byte
        strings.

    """
    result = []
    for string in string_list:
        result.append(line2dict(string, mode))
    return result
