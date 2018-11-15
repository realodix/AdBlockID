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

from __future__ import unicode_literals

import pytest

from abp.filters import (
    parse_line, parse_filterlist, ParseError,
    SELECTOR_TYPE as ST, FILTER_ACTION as FA, FILTER_OPTION as OPT,
)
from abp.filters.parser import Comment, Metadata, Header


def test_parse_empty():
    line = parse_line('    ')
    assert line.type == 'emptyline'


@pytest.mark.parametrize('filter_text, expected', {
    # Blocking filters with patterns and regexps and blocking exceptions.
    '*asdf*d**dd*': {
        'selector': {'type': ST.URL_PATTERN, 'value': '*asdf*d**dd*'},
        'action': FA.BLOCK,
    },
    '@@|*asd|f*d**dd*|': {
        'selector': {'type': ST.URL_PATTERN, 'value': '|*asd|f*d**dd*|'},
        'action': FA.ALLOW,
    },
    '/ddd|f?a[s]d/': {
        'selector': {'type': ST.URL_REGEXP, 'value': 'ddd|f?a[s]d'},
        'action': FA.BLOCK,
    },
    '@@/ddd|f?a[s]d/': {
        'selector': {'type': ST.URL_REGEXP, 'value': 'ddd|f?a[s]d'},
        'action': FA.ALLOW,
    },
    # Blocking filters with some options.
    'bla$match-case,~script,domain=foo.com|~bar.com,sitekey=foo': {
        'selector': {'type': ST.URL_PATTERN, 'value': 'bla'},
        'action': FA.BLOCK,
        'options': [
            (OPT.MATCH_CASE, True),
            (OPT.SCRIPT, False),
            (OPT.DOMAIN, [('foo.com', True), ('bar.com', False)]),
            (OPT.SITEKEY, ['foo']),
        ],
    },
    '@@http://bla$~script,~other,sitekey=foo|bar': {
        'selector': {'type': ST.URL_PATTERN, 'value': 'http://bla'},
        'action': FA.ALLOW,
        'options': [
            (OPT.SCRIPT, False),
            (OPT.OTHER, False),
            (OPT.SITEKEY, ['foo', 'bar']),
        ],
    },
    "||foo.com^$csp=script-src 'self' * 'unsafe-inline',script,sitekey=foo,"
    + 'other,match-case,domain=foo.com': {
        'selector': {'type': ST.URL_PATTERN, 'value': '||foo.com^'},
        'action': FA.BLOCK,
        'options': [
            (OPT.CSP, "script-src 'self' * 'unsafe-inline'"),
            ('script', True),
            ('sitekey', ['foo']),
            ('other', True),
            ('match-case', True),
            ('domain', [('foo.com', True)]),
        ],
    },
    '@@bla$script,other,domain=foo.com|~bar.foo.com,csp=c s p': {
        'selector': {'type': ST.URL_PATTERN, 'value': 'bla'},
        'action': FA.ALLOW,
        'options': [
            ('script', True),
            ('other', True),
            ('domain', [('foo.com', True), ('bar.foo.com', False)]),
            ('csp', 'c s p'),
        ],
    },
    '||content.server.com/files/*.php$rewrite=$1': {
        'selector': {'type': ST.URL_PATTERN,
                     'value': '||content.server.com/files/*.php'},
        'action': FA.BLOCK,
        'options': [
            ('rewrite', '$1'),
        ],
    },
    # Element hiding filters and exceptions.
    '##ddd': {
        'selector': {'type': ST.CSS, 'value': 'ddd'},
        'action': FA.HIDE,
        'options': [],
    },
    '#@#body > div:first-child': {
        'selector': {'type': ST.CSS, 'value': 'body > div:first-child'},
        'action': FA.SHOW,
        'options': [],
    },
    'foo,~bar##ddd': {
        'options': [(OPT.DOMAIN, [('foo', True), ('bar', False)])],
    },
    # Element hiding emulation filters (extended CSS).
    'foo,~bar#?#:-abp-properties(abc)': {
        'selector': {'type': ST.XCSS, 'value': ':-abp-properties(abc)'},
        'action': FA.HIDE,
        'options': [(OPT.DOMAIN, [('foo', True), ('bar', False)])],
    },
    'foo.com#?#aaa :-abp-properties(abc) bbb': {
        'selector': {
            'type': ST.XCSS,
            'value': 'aaa :-abp-properties(abc) bbb',
        },
    },
    '#?#:-abp-properties(|background-image: url(data:*))': {
        'selector': {
            'type': ST.XCSS,
            'value': ':-abp-properties(|background-image: url(data:*))',
        },
        'options': [],
    },
}.items())
def test_parse_filters(filter_text, expected):
    """Parametric test for filter parsing."""
    parsed = parse_line(filter_text)
    assert parsed.type == 'filter'
    assert parsed.text == filter_text
    for attribute, expected_value in expected.items():
        assert getattr(parsed, attribute) == expected_value


def test_parse_comment():
    line = parse_line('! Block foo')
    assert line.type == 'comment'
    assert line.text == 'Block foo'


def test_parse_instruction():
    line = parse_line('%include foo:bar/baz.txt%')
    assert line.type == 'include'
    assert line.target == 'foo:bar/baz.txt'


def test_parse_bad_instruction():
    with pytest.raises(ParseError):
        parse_line('%foo bar%')


def test_parse_start():
    # Header-line lines are headers.
    assert parse_line('[Adblock Plus 1.1]', 'start').type == 'header'
    # Even if they have extra characters around.
    assert parse_line('foo[Adblock Plus 1.1] bar', 'start').type == 'header'

    # But the inside of the header needs to be right.
    assert parse_line('[Adblock Minus 1.1]', 'start').type == 'filter'
    # Really right!
    assert parse_line('[Adblock 1.1]', 'start').type == 'filter'
    # Otherwise it's just considered a filter.

    # Metadata-like lines are metadata.
    assert parse_line('! Foo: bar', 'metadata').type == 'metadata'


def test_parse_metadata():
    # Header-like lines are just filters.
    assert parse_line('[Adblock 1.1]', 'metadata').type == 'filter'
    # Metadata-like lines are metadata.
    assert parse_line('! Foo: bar', 'metadata').type == 'metadata'


def test_parse_body():
    # Header-like lines are just filters.
    assert parse_line('[Adblock 1.1]', 'body').type == 'filter'
    # Metadata-like lines are comments.
    assert parse_line('! Foo: bar', 'body').type == 'comment'
    # But there's an exception for the checksum.
    assert parse_line('! Checksum: 42', 'body').type == 'metadata'


def test_parse_invalid_position():
    with pytest.raises(ValueError):
        parse_line('', 'nonsense')


def test_parse_filterlist():
    result = parse_filterlist(['[Adblock Plus 1.1]',
                               ' ! Last modified: 26 Jul 2018 02:10 UTC ',
                               '! Homepage  :  http://aaa.com/b',
                               '||example.com^',
                               '! Checksum: OaopkIiiAl77sSHk/VAWDA',
                               '! Note: bla bla'])

    assert next(result) == Header('Adblock Plus 1.1')
    # Check that trailing space is not stripped (like in ABP).
    assert next(result) == Metadata('Last modified', '26 Jul 2018 02:10 UTC ')
    assert next(result) == Metadata('Homepage', 'http://aaa.com/b')
    assert next(result).type == 'filter'
    assert next(result) == Metadata('Checksum', 'OaopkIiiAl77sSHk/VAWDA')
    assert next(result).type == 'comment'

    with pytest.raises(StopIteration):
        next(result)


def test_exception_timing():
    result = parse_filterlist(['! good line', '%bad line%'])
    assert next(result) == Comment('good line')
    with pytest.raises(ParseError):
        next(result)


def test_parse_line_bytes():
    line = parse_line(b'! \xc3\xbc')
    assert line.text == '\xfc'
