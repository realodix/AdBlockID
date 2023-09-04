""" Parser for ABP filterlist format. """

from __future__ import unicode_literals

import re
from collections import namedtuple

__all__ = [
    'ParseError',
    'parse_filterlist',
    'parse_line',
]


def _line_type(name, field_names, format_string):
    """ Define a line type.

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


Header = _line_type('lt_header', 'version', '[{.version}]')
EmptyLine = _line_type('lt_emptyLine', '', '')
Comment = _line_type('lt_comment', 'text', '{.text}')
Metadata = _line_type('lt_metadata', 'key value', '! {0.key}: {0.value}')
Filter = _line_type('lt_filter', 'text', '{.text}')
Include = _line_type('lt_include', 'target', '%include {0.target}%')


RE_METADATA = re.compile(r'\s*!\s*([\w\-\s]*\w)\s*:\s*(.*)')
RE_INCLUDE = re.compile(r'%include\s+(.+)%')
RE_HEADER = re.compile(r'\[(Adblock(?:\s*Plus\s*[\d\.]+?)?)\]', flags=re.I)


def parse_filterlist(lines):
    """ Parse filter list from an iterable.

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

    position = 'pHeader'

    for line in lines:
        parsed_line = parse_line(line, position)
        yield parsed_line

        if position != 'pBody' and parsed_line.type in {'lt_header', 'lt_metadata'}:
            # Continue parsing metadata until it's over...
            position = 'pMetadata'
        else:
            # ...then switch to parsing the body.
            position = 'pBody'


def parse_line(line, position='body'):
    """ Parse one line of a filter list.

    Tipe line yang dikenali oleh parser bergantung pada posisinya.
    - pBody    : Parser hanya mengenali filter, komentar, instruksi pemrosesan, dan
                 baris kosong.
    - pMetadata: pBody + lt_metadata.
    - pHeader  : pBody + lt_header.

    Note: Line metadata checksum dikenali di semua posisi untuk backwards compatibility.
    Secara historis, checksum ada di bagian paling bawah filter list. Checksum sudah tidak
    digunakan oleh ad blocker modern, tetapi untuk menghapusnya (di filter_combiner.combiner), Kita
    harus memastikan untuk tetap menguraikannya terlepas dari posisinya ada dimana di dalam
    filter list.

    Parameters
    ----------
    line : str
        Line of a filter list.
    position : str
        Position in the filter list, one of "pHeader", "pMetadata" or "pBody"
        (default is "pBody").

    Returns
    -------
    namedtuple
        Parsed line (see `_line_type`).

    Raises
    ------
    ParseError
        ParseError: If the line can't be parsed.

    """

    positions = {'pBody', 'pHeader', 'pMetadata'}

    if position not in positions:
        raise ValueError('position should be one of {}'.format(positions))

    if isinstance(line, type(b'')):
        line = line.decode('utf-8')

    stripped = line.strip()

    if stripped == '':
        return EmptyLine()

    if position == 'pHeader':
        match = RE_HEADER.search(line)
        if match:
            return Header(match.group(1))

    # Comment syntax (rules starting with #)
    if re.search('^!$|^![^#]+|!#(\s.+)?$'      # Standart comment
                 '|^#$|^#[^#@$?%]|^##(\s|##)', # uBO special comment
                 stripped):
        match = RE_METADATA.match(line)
        if match:
            key, value = match.groups()
            if position != 'pBody' or key.lower() == 'checksum':
                return Metadata(key, value)
        return Comment(stripped)

    if stripped.startswith('%include') and stripped.endswith('%'):
        return _parse_instruction(stripped)

    return Filter(stripped)


def _parse_instruction(text):
    match = RE_INCLUDE.match(text)
    if not match:
        raise ParseError('Unrecognized instruction', text)
    return Include(match.group(1))


class ParseError(Exception):
    """ Exception thrown by the parser when it encounters invalid input.

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
