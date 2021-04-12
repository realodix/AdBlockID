from __future__ import unicode_literals
from afc.version import __version__
import datetime, subprocess
import argparse, io, itertools, logging, sys, time
from .parser import parse_filterlist, Metadata
from .sources import FSSource, TopSource, WebSource, NotFound

__all__ = ['main','IncludeError', 'MissingHeader', 'render_filterlist']

_logger = logging.getLogger(__name__)


def parse_args():
    """Command line script for rendering Adblock Plus filter lists."""
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


def render_filterlist(name, sources, top_source=None):
    """Produce filter list from fragments.

    Parameters
    ----------
    name : str
        Name of the top level fragment.
    sources : dict of str -> Source
        Sources for loading included fragments.
    top_source : Source
        The source used to load the top level fragment.

    Returns
    -------
    iterable of namedtuple (see `_line_type` in parser.py)
        Rendered filter list.

    Raises
    ------
    IncludeError
        When an include error can't be processed.
    ParseError
        When any of the fragments contain lines that can't be parsed.
    MissingHeader
        If the top level fragment doesn't start with a valid header. This would lead to
        rendering an invalid filter list, so we immediately abort.

    """
    _logger.info('Rendering: %s', name)
    lines, default_source = _get_and_parse_fragment(name, sources, top_source)
    lines = _process_includes(sources, default_source, [name], lines)
    for proc in [_timestamps, _compiler_info, _version, _remove_checksum,
                 _validate]:
        lines = proc(lines)
    return lines


def _get_and_parse_fragment(name, sources, default_source, include_stack=[]):
    """Retrieve and parse fragment.

    Returns
    -------
    tuple (iterator of str, Source)
        First part is the content of the fragment line by line; second part is the default
        source to be used for included fragments.

    """
    if ':' in name:
        source_name, name_in_source = name.split(':', 1)
        try:
            source = sources[source_name]
        except KeyError:
            raise IncludeError("Unknown source: '{}'".format(source_name),
                               include_stack)
    else:
        source, name_in_source = default_source, name

    if source is None:
        raise IncludeError("Source name is absent in: '{}'".format(name),
                           include_stack)

    return (parse_filterlist(source.get(name_in_source)),
            source if source.is_inheritable else None)


def _process_includes(sources, default_source, parent_include_stack, lines):
    """Replace include instructions with the lines of included fragment."""
    for line in lines:
        if line.type == 'include':
            name = line.target
            include_stack = parent_include_stack + [name]
            if name in parent_include_stack:
                raise IncludeError('Include loop encountered', include_stack)

            try:
                included, inherited_source = _get_and_parse_fragment(
                    name, sources, default_source, include_stack)
                all_included = _process_includes(
                    sources, inherited_source, include_stack, included)

                _logger.info('- including: %s', name)

                for line in all_included:
                    if line.type not in {'header', 'metadata'}:
                        yield line
            except (NotFound, ValueError) as exc:
                raise IncludeError(exc, include_stack)
        # Cleanup blank lines and comment
        elif line.type == 'emptyline' or line.type == 'comment':
            continue
        else:
            yield line


def _version(lines):
    """Insert metadata comment with version (a.k.a. date)."""
    first_line, rest = _first_and_rest(lines)

    # year.day_of_the_year.v_build
    # v_build = (datetime.datetime.utcnow().hour*60)+datetime.datetime.utcnow().minute
    # version = Metadata('Version', time.strftime('%y.%j.{}'.format(v_build), time.gmtime()))

    # year.month.number_of_commits_in_month
    numberOfCommitsInMonth = subprocess.Popen(
        [
            'git', 'rev-list', 'HEAD', '--count', '--after="{} days"' '"+%Y-%m-%dT23:59"'
            .format(datetime.datetime.now().day)
        ],
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    version = Metadata(
        'Version',
        time.strftime('%y.X%m.{}'.format(numberOfCommitsInMonth.stdout.read().strip()),
                      time.gmtime()).replace('X0', 'X').replace('X', '')
        # https://stackoverflow.com/a/5900593
    )

    return itertools.chain([first_line, version], rest)


def _timestamps(lines):
    """Convert timestamp markers into actual timestamps."""
    for line in lines:
        if line.type == 'metadata' and line.value == '%timestamp%':
            timestamp = time.strftime('%d %b %Y %H:%M UTC', time.gmtime())
            yield Metadata(line.key, timestamp)
        else:
            yield line


def _compiler_info(lines):
    pa_abid = 'AdBlockID FC v{}'.format(__version__)

    for line in lines:
        if line.type != 'emptyline':
            pa_abid
        yield line

    yield Metadata('Compiler', pa_abid)


def _first_and_rest(iterable):
    """Return the first item from the iterable and the rest as an iterator."""
    iterator = iter(iterable)
    first_item = next(iterator)
    return first_item, iterator


def _remove_checksum(lines):
    """Remove metadata comments giving a checksum.

    Adblock Plus is no longer verifying checksums, so we don't have to calculate the
    checksum for the resulting filter list. But we have to strip them for compatibility
    with older versions of Adblock Plus and other ad blockers which might still verify a
    checksum if given.
    """
    for line in lines:
        if line.type != 'metadata' or line.key.lower() != 'checksum':
            yield line


def _validate(lines):
    """Validate the final list."""
    first_line, rest = _first_and_rest(lines)
    if first_line.type != 'header':
        raise MissingHeader('No header found at the beginning of the input.')
    return itertools.chain([first_line], rest)


class IncludeError(Exception):
    """Error in processing include instruction."""

    def __init__(self, error, stack):
        stack_str = ' from '.join(map("'{}'".format, reversed(stack)))
        if stack_str:
            error = '{} when including {}'.format(error, stack_str)
        Exception.__init__(self, error)


class MissingHeader(Exception):
    """First line of the result is not a valid header."""
