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

"""Functional tests for the diff script."""

from __future__ import unicode_literals

import pytest
import subprocess
import io

from test_differ import BASE, LATEST


@pytest.fixture
def rootdir(tmpdir):
    """Directory with example filter lists."""
    rootdir = tmpdir.join('root')
    rootdir.mkdir()
    rootdir.join('base.txt').write_text(BASE, encoding='utf8')
    rootdir.join('latest.txt').write_text(LATEST, encoding='utf8')

    return rootdir


@pytest.fixture
def dstfile(tmpdir):
    """Destination file for saving the diff output."""
    return tmpdir.join('dst')


def run_script(*args, **kw):
    """Run diff rendering script with given arguments and return its output."""
    cmd = ['fldiff'] + list(args)

    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                            **kw)
    stdout, stderr = proc.communicate()
    return proc.returncode, stderr.decode('utf-8'), stdout.decode('utf-8')


def test_diff_with_outfile(rootdir, dstfile):
    run_script(str(rootdir.join('base.txt')),
               str(rootdir.join('latest.txt')),
               str(dstfile))
    with io.open(str(dstfile), encoding='utf-8') as dst:
        result = dst.read()
    assert '+ &ad_channel=\xa3' in result


def test_no_outfile(rootdir):
    _, _, out = run_script(str(rootdir.join('base.txt')),
                           str(rootdir.join('latest.txt')))
    assert '[Adblock Plus Diff]' in out


def test_no_base_file(rootdir):
    code, err, _ = run_script('wrong.txt', str(rootdir.join('latest.txt')))
    assert code == 1
    assert 'No such file or directory' in err


def test_no_latest_file(rootdir):
    code, err, _ = run_script(str(rootdir.join('base.txt')), 'wrong.txt')
    assert code == 1
    assert 'No such file or directory' in err


def test_diff_to_self(rootdir):
    _, _, out = run_script(str(rootdir.join('latest.txt')),
                           str(rootdir.join('latest.txt')))
    assert out == '[Adblock Plus Diff]\n'
