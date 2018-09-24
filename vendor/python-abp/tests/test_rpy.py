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

"""Functional tests for testing rPython integration."""
from __future__ import unicode_literals

from collections import namedtuple
import pytest
import sys

from abp.filters.rpy import tuple2dict, line2dict


_SAMPLE_TUPLE = namedtuple('tuple', 'foo,bar')

_TEST_EXAMPLES = {
    'header': {
        'in': b'[Adblock Plus 2.0]',
        'out': {
            b'type': b'Header',
            b'version': b'Adblock Plus 2.0',
        },
    },
    'metadata': {
        'in': b'! Title: Example list',
        'out': {
            b'type': b'Metadata',
            b'key': b'Title',
            b'value': b'Example list',
        },
    },
    'comment': {
        'in': b'! Comment',
        'out': {
            b'type': b'Comment',
            b'text': b'Comment',
        },
    },
    'empty': {
        'in': b'',
        'out': {
            b'type': b'EmptyLine',
        },
    },
    'include': {
        'in': b'%include www.test.py/filtelist.txt%',
        'out': {
            b'type': b'Include',
            b'target': b'www.test.py/filtelist.txt',
        },
    },
    'filter_single': {
        'in': b'foo.com##div#ad1',
        'out': {
            b'type': b'Filter',
            b'text': b'foo.com##div#ad1',
            b'selector': {b'type': b'css', b'value': b'div#ad1'},
            b'action': b'hide',
            b'options': [(b'domain', [(b'foo.com', True)])],
        },
    },
    'filter_multiple': {
        'in': b'foo.com,bar.com##div#ad1',
        'out': {
            b'type': b'Filter',
            b'text': b'foo.com,bar.com##div#ad1',
            b'selector': {b'type': b'css', b'value': b'div#ad1'},
            b'action': b'hide',
            b'options': [(b'domain', [(b'foo.com', True), (b'bar.com',
                                                           True)])],
        },
    },
}


def check_data_utf8(data):
    """Check if all the strings in a dict are encoded as unicode.

    Parameters
    ----------
    data: dict
        The dictionary to be checked

    Raises
    -------
    AssertionError
        If any of the strings encountered are not unicode

    """
    if isinstance(data, dict):
        for key, value in data.items():
            check_data_utf8(key)
            check_data_utf8(value)
    elif isinstance(data, (list, tuple)):
        for item in data:
            check_data_utf8(item)
    elif isinstance(data, type('')):
        raise AssertionError('{} is str. Expected bytes.'.format(data))


@pytest.mark.parametrize('foo,bar', [
    ('test_foo', 1),
    ({'foofoo': 'test', 'foobar': 2}, [1, 2, 3]),
    ((1,), [('a', True), ('b', False)]),
])
def test_tuple2dict(foo, bar):
    """Test that dicts are produced correctly from a named tuple."""
    data = _SAMPLE_TUPLE(foo=foo, bar=bar)
    exp = {'foo': foo, 'bar': bar, 'type': 'tuple'}

    result = tuple2dict(data)

    assert exp == result


@pytest.mark.skipif(sys.version.startswith('3.'), reason='Redundant on py3+.')
@pytest.mark.parametrize('line_type', _TEST_EXAMPLES.keys())
def test_line2dict_encoding(line_type):
    """Test that the resulting object has all strings encoded as utf-8.

    These tests will only be run on Python2.*. On Python3.*, these test
    cases are covered by test_line2dict() below.
    """
    data = line2dict(_TEST_EXAMPLES[line_type]['in'])
    check_data_utf8(data)


@pytest.mark.parametrize('line_type', list(_TEST_EXAMPLES.keys()))
def test_line2dict_format(line_type):
    """Test that the API result has the appropriate format.

    Checks for both keys and datatypes.
    """
    position = 'start' if line_type in {'header', 'metadata'} else 'body'
    data = line2dict(_TEST_EXAMPLES[line_type]['in'], position)

    assert data == _TEST_EXAMPLES[line_type]['out']
