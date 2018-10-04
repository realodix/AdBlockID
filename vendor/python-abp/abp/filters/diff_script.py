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

"""Command line script for rendering Adblock Plus filter list diffs."""

from __future__ import print_function

import argparse
import io
import sys

from .renderer import render_diff

__all__ = ['main']


def parse_args():
    parser = argparse.ArgumentParser(description='Render a filter list diff.')
    parser.add_argument(
        'base', help='the older filter list that needs to be updated',
        nargs='?')
    parser.add_argument(
        'latest', help='the most recent version of the filter list',
        nargs='?')
    parser.add_argument(
        'outfile', help='output file for filter list diff',
        default='-', nargs='?')
    return parser.parse_args()


def main():
    """Entry point for the diff rendering script (fldiff)."""
    args = parse_args()

    with io.open(args.base, 'r', encoding='utf-8') as base, \
            io.open(args.latest, 'r', encoding='utf-8') as latest:

        lines = render_diff(base, latest)
        if args.outfile == '-':
            outfile = io.open(sys.stdout.fileno(), 'w',
                              closefd=False,
                              encoding=sys.stdout.encoding or 'utf-8')
        else:
            outfile = io.open(args.outfile, 'w', encoding='utf-8')

        with outfile:
            for line in lines:
                print(line, file=outfile)
