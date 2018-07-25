# This file is part of Adblock Plus <https://adblockplus.org/>,
# Copyright (C) 2006-present eyeo GmbH
#
# Adblock Plus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Adblock Plus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Adblock Plus.  If not, see <http://www.gnu.org/licenses/>.

"""Parser for ABP filterlist format."""

from __future__ import unicode_literals

import re
from collections import namedtuple

__all__ = [
    'FILTER_ACTION',
    'FILTER_OPTION',
    'SELECTOR_TYPE',
    'ParseError',
    'parse_filterlist',
    'parse_line',
]


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


# Constants related to filters (see https://adblockplus.org/filters).
class SELECTOR_TYPE:  # flake8: noqa (this is a namespace of constants).
    """Selector type constants."""
    URL_PATTERN = 'url-pattern'  # Normal URL patterns.
    URL_REGEXP = 'url-regexp'    # Regular expressions for URLs.
    CSS = 'css'                  # CSS selectors for hiding filters.
    XCSS = 'extended-css'        # Extended CSS selectors (to emulate CSS4).
    ABP_SIMPLE = 'abp-simple'    # Simplified element hiding syntax.


class FILTER_ACTION:  # flake8: noqa (this is a namespace of constants).
    """Filter action constants."""
    BLOCK = 'block'              # Block the request.
    ALLOW = 'allow'              # Allow the request (whitelist).
    HIDE = 'hide'                # Hide selected element(s).
    SHOW = 'show'                # Show selected element(s) (whitelist).


class FILTER_OPTION:  # flake8: noqa (this is a namespace of constants).
    """Filter option constants."""
    # Resource types.
    OTHER = 'other'
    SCRIPT = 'script'
    IMAGE = 'image'
    STYLESHEET = 'stylesheet'
    OBJECT = 'object'
    SUBDOCUMENT = 'subdocument'
    DOCUMENT = 'document'
    WEBSOCKET = 'websocket'
    WEBRTC = 'webrtc'
    PING = 'ping'
    XMLHTTPREQUEST = 'xmlhttprequest'
    OBJECT_SUBREQUEST = 'object-subrequest'
    MEDIA = 'media'
    FONT = 'font'
    POPUP = 'popup'
    GENERICBLOCK = 'genericblock'
    ELEMHIDE = 'elemhide'
    GENERICHIDE = 'generichide'

    # Deprecated resource types.
    BACKGROUND = 'background'
    XBL = 'xbl'
    DTD = 'dtd'

    # Other options.
    MATCH_CASE = 'match-case'
    DOMAIN = 'domain'
    THIRD_PARTY = 'third-party'
    COLLAPSE = 'collapse'
    SITEKEY = 'sitekey'
    DONOTTRACK = 'donottrack'


def _line_type(name, field_names, format_string):
    """Define a line type.

    Parameters
    ----------
    name: str
        The name of the line type to define.
    field_names: str or list
        A sequence of field names or one space-separated string that contains
        all field names.
    format_string: str
        A format specifier for converting this line type back to string
        representation.

    Returns
    -------
    class
        Class created with `namedtuple` that has `.type` set to lowercased
        `name` and supports conversion back to string with `.to_string()`
        method.

    """
    lt = namedtuple(name, field_names)
    lt.type = name.lower()
    lt.to_string = lambda self: format_string.format(self)
    return lt


Header = _line_type('Header', 'version', '[{.version}]')
EmptyLine = _line_type('EmptyLine', '', '')
Comment = _line_type('Comment', 'text', '! {.text}')
Metadata = _line_type('Metadata', 'key value', '! {0.key}: {0.value}')
Filter = _line_type('Filter', 'text selector action options', '{.text}')
Include = _line_type('Include', 'target', '%include {0.target}%')


METADATA_REGEXP = re.compile(r'!\s*(\w+)\s*:\s*(.*)')
METADATA_KEYS = {'Homepage', 'Title', 'Expires', 'Checksum', 'Redirect',
                 'Version'}
INCLUDE_REGEXP = re.compile(r'%include\s+(.+)%')
HEADER_REGEXP = re.compile(r'\[(Adblock(?:\s*Plus\s*[\d\.]+?)?)\]', flags=re.I)
HIDING_FILTER_REGEXP = re.compile(r'^([^/*|@"!]*?)#([@?])?#(.+)$')
FILTER_OPTIONS_REGEXP = re.compile(
    r'\$(~?[\w-]+(?:=[^,\s]+)?(?:,~?[\w-]+(?:=[^,\s]+)?)*)$'
)


def _parse_comment(text):
    match = METADATA_REGEXP.match(text)
    if match and match.group(1) in METADATA_KEYS:
        return Metadata(match.group(1), match.group(2))
    return Comment(text[1:].strip())


def _parse_header(text):
    match = HEADER_REGEXP.match(text)
    if not match:
        raise ParseError('Malformed header', text)
    return Header(match.group(1))


def _parse_instruction(text):
    match = INCLUDE_REGEXP.match(text)
    if not match:
        raise ParseError('Unrecognized instruction', text)
    return Include(match.group(1))


def _parse_option(option):
    if '=' in option:
        return option.split('=', 1)
    if option.startswith('~'):
        return option[1:], False
    return option, True


def _parse_filter_option(option):
    name, value = _parse_option(option)

    # Handle special cases of multivalued options.
    if name == FILTER_OPTION.DOMAIN:
        value = [_parse_option(o) for o in value.split('|')]
    elif name == FILTER_OPTION.SITEKEY:
        value = value.split('|')

    return name, value


def _parse_filter_options(options):
    return [_parse_filter_option(o) for o in options.split(',')]


def _parse_blocking_filter(text):
    # Based on RegExpFilter.fromText in lib/filterClasses.js
    # in https://hg.adblockplus.org/adblockpluscore.
    action = FILTER_ACTION.BLOCK
    options = []
    selector = text

    if selector.startswith('@@'):
        action = FILTER_ACTION.ALLOW
        selector = selector[2:]

    if '$' in selector:
        opt_match = FILTER_OPTIONS_REGEXP.search(selector)
        if opt_match:
            selector = selector[:opt_match.start(0)]
            options = _parse_filter_options(opt_match.group(1))

    if (len(selector) > 1 and
            selector.startswith('/') and selector.endswith('/')):
        selector = {'type': SELECTOR_TYPE.URL_REGEXP, 'value': selector[1:-1]}
    else:
        selector = {'type': SELECTOR_TYPE.URL_PATTERN, 'value': selector}

    return Filter(text, selector, action, options)


def _parse_hiding_filter(text, domain, type_flag, selector_value):
    selector = {'type': SELECTOR_TYPE.CSS, 'value': selector_value}
    action = FILTER_ACTION.HIDE
    options = []

    if type_flag == '@':
        action = FILTER_ACTION.SHOW
    elif type_flag == '?':
        selector['type'] = SELECTOR_TYPE.XCSS

    if domain:
        domains = [_parse_option(d) for d in domain.split(',')]
        options.append((FILTER_OPTION.DOMAIN, domains))

    return Filter(text, selector, action, options)


def parse_filter(text):
    """Parse one filter.

    Parameters
    ----------
    text : str
        Filter to parse in ABP filter list syntax.

    Returns
    -------
    namedtuple
        Parsed filter.

    """
    if '#' in text:
        match = HIDING_FILTER_REGEXP.search(text)
        if match:
            return _parse_hiding_filter(text, *match.groups())
    return _parse_blocking_filter(text)


def parse_line(line_text):
    """Parse one line of a filter list.

    Parameters
    ----------
    line_text : str
        Line of a filter list.

    Returns
    -------
    namedtuple
        Parsed line (see `_line_type`).

    Raises
    ------
    ParseError
        ParseError: If the line can't be parsed.
    """
    if isinstance(line_text, type(b'')):
        line_text = line_text.decode('utf-8')

    content = line_text.strip()

    if content == '':
        line = EmptyLine()
    elif content.startswith('!'):
        line = _parse_comment(content)
    elif content.startswith('%') and content.endswith('%'):
        line = _parse_instruction(content)
    elif content.startswith('[') and content.endswith(']'):
        line = _parse_header(content)
    else:
        line = parse_filter(content)

    assert line.to_string().replace(' ', '') == content.replace(' ', '')
    return line


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
    for line in lines:
        yield parse_line(line)
