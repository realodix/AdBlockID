"""Helping methods for filterhit-related statistics."""

import csv


def load_filterhit_statistics(path, sources=None):
    """Load filterhit statistics from a csv file.

    Parameters
    ----------
    path: str
        Path to the csv file with the filterhit statistics.
    sources: iterable of str
        With the filter sources we're interested in. If not None, only filters
        from these sources will be included in the result.

    Returns
    -------
    generator of dict
        With the csv entries.

    """
    integer_cols = ['onehour_sessions', 'hits', 'domains', 'rootdomains']

    with open(path) as csvstream:
        reader = csv.DictReader(csvstream)

        for entry in reader:
            if sources and entry['source'] not in sources:
                continue
            for col in integer_cols:
                try:
                    entry[col] = int(entry[col])
                except KeyError:
                    continue

            yield entry
