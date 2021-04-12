"""Parser for ABP filterlist format."""

from __future__ import unicode_literals

import re
from collections import namedtuple

__all__ = [
    'ParseError',
    'parse_filterlist',
    'parse_line',
]


def _line_type(name, field_names, format_string):
    """Define a line type.

    Parameters
    ----------
    name: str
        The name of the line type to define.
    field_names: str or list
        A sequence of field names or one space-separated string that contains all field
        names.
    format_string: str
        A format specifier for converting this line type back to string representation.

    Returns
    -------
    class
        Class created with `namedtuple` that has `.type` set to lowercased `name` and
        supports conversion back to string with `.to_string()` method.

    """
    lt = namedtuple(name, field_names)
    lt.type = name.lower()
    lt.to_string = lambda self: format_string.format(self)
    return lt


Header = _line_type('Header', 'version', '[{.version}]')
EmptyLine = _line_type('EmptyLine', '', '')
Comment = _line_type('Comment', 'text', '{.text}')
Metadata = _line_type('Metadata', 'key value', '! {0.key}: {0.value}')
Filter = _line_type('Filter', 'text', '{.text}')
Include = _line_type('Include', 'target', '%include {0.target}%')


METADATA_REGEXP = re.compile(r'\s*!\s*([\w\-\s]*\w)\s*:\s*(.*)')
INCLUDE_REGEXP = re.compile(r'%include\s+(.+)%')
HEADER_REGEXP = re.compile(r'\[(Adblock(?:\s*Plus\s*[\d\.]+?)?)\]', flags=re.I)


def parse_filterlist(lines):
    """Parse filter list from an iterable.

    Parameters
    ----------
    lines: iterable of str
        Lines of the filter list.

    Returns
    -------
    iterator of namedtuple
        Parsed lines of the filter list.

    Raises
    ------
    ParseError
        Thrown during iteration for invalid filter list lines.
    TypeError
        If `lines` is not iterable.

    """
    position = 'start'

    for line in lines:
        parsed_line = parse_line(line, position)
        yield parsed_line

        if position != 'body' and parsed_line.type in {'header', 'metadata'}:
            # Continue parsing metadata until it's over...
            position = 'metadata'
        else:
            # ...then switch to parsing the body.
            position = 'body'


def parse_line(line, position='body'):
    """Parse one line of a filter list.

    The types of lines that that the parser recognizes depend on the position. If
    position="body", the parser only recognizes filters, comments, processing instructions
    and empty lines. If position="metadata", it in addition recognizes metadata. If
    position="start", it also recognizes headers.

    Note: Checksum metadata lines are recognized in all positions for backwards
    compatibility. Historically, checksums can occur at the bottom of the filter list.
    They are are no longer used by Adblock Plus, but in order to strip them (in
    afc.filters.renderer), we have to make sure to still parse them regardless of their
    position in the filter list.

    Parameters
    ----------
    line : str
        Line of a filter list.
    position : str
        Position in the filter list, one of "start", "metadata" or "body"
        (default is "body").

    Returns
    -------
    namedtuple
        Parsed line (see `_line_type`).

    Raises
    ------
    ParseError
        ParseError: If the line can't be parsed.

    """
    positions = {'body', 'start', 'metadata'}
    if position not in positions:
        raise ValueError('position should be one of {}'.format(positions))

    if isinstance(line, type(b'')):
        line = line.decode('utf-8')

    stripped = line.strip()

    if stripped == '':
        return EmptyLine()

    if position == 'start':
        match = HEADER_REGEXP.search(line)
        if match:
            return Header(match.group(1))

    # ABP comments and uBo comments (rules starting with #)
    if re.search('^!$|^![^#+]'                 # comment
                 '|^#$|^#[^#@$?%]|^##(\s|##)', # uBo comment
                 stripped):
        match = METADATA_REGEXP.match(line)
        if match:
            key, value = match.groups()
            if position != 'body' or key.lower() == 'checksum':
                return Metadata(key, value)
        return Comment(stripped)

    if stripped.startswith('%include') and stripped.endswith('%'):
        return _parse_instruction(stripped)

    return Filter(stripped)


def _parse_instruction(text):
    match = INCLUDE_REGEXP.match(text)
    if not match:
        raise ParseError('Unrecognized instruction', text)
    return Include(match.group(1))


class ParseError(Exception):
    """Exception thrown by the parser when it encounters invalid input.

    Parameters
    ----------
    error : str
        Description of the error.
    text : str
        The source text that caused an error.

    """

    def __init__(self, error, text):
        Exception.__init__(self, '{} in "{}"'.format(error, text))
        self.text = text
        self.error = error
