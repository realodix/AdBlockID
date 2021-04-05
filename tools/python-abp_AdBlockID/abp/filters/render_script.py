"""Command line script for rendering Adblock Plus filter lists."""

import argparse
import io
import logging
import sys

from .sources import FSSource, TopSource, WebSource, NotFound
from .renderer import render_filterlist, IncludeError, MissingHeader

__all__ = ['main']


def parse_args():
    parser = argparse.ArgumentParser(description='Render a filter list.')
    parser.add_argument(
        'infile', help='top level filter list fragment from which the '
        'rendering starts', default='-', nargs='?')
    parser.add_argument('outfile', help='output filter list file',
                        default='-', nargs='?')
    parser.add_argument(
        '-i', '--include', action='append', default=[], metavar='NAME=PATH',
        help='define include path (could be given multiple times)')
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help='log included files and URLs')
    return parser.parse_args()


def main():
    """Entry point for the rendering script (flrender)."""
    sources = {
        'http': WebSource('http'),
        'https': WebSource('https'),
    }
    args = parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                            format='%(message)s')

    for include_path in args.include:
        name, path = include_path.split('=', 1)
        sources[name] = FSSource(path)

    try:
        lines = render_filterlist(args.infile, sources, TopSource())
        if args.outfile == '-':
            for line in lines:
                sys.stdout.write(line.to_string() + '\n')
        else:
            with io.open(args.outfile, 'w', encoding='utf-8') as out_fp:
                for line in lines:
                    out_fp.write(line.to_string() + '\n')
    except (MissingHeader, NotFound, IncludeError) as exc:
        sys.exit(exc)
