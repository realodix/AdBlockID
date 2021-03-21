#!/usr/bin/env python3
"""
FOP (Filter Orderer and Preener) AdBlockID

Adjusted for AdBlockID based on FOP RU AdList v3.921
"""

import os, re, subprocess, sys
import sort, var


""" Print a greeting message and run FOP in the directories specified via the command
    line, or the current working directory if no arguments have been passed."""
def start ():
    greeting = "FOP AdBlockID v{version}".format(version = var.VERSION)
    characters = len(str(greeting))
    print("=" * characters)
    print(greeting)
    print("=" * characters)

    # Convert the directory names to absolute references and visit each unique location
    places = sys.argv[1:]
    if places:
        places = [os.path.abspath(place) for place in places]
        for place in sorted(set(places)):
            main(place)
            print()
    else:
        main(os.getcwd())



""" Find and sort all the files in a given directory, committing changes to a repository
    if one exists."""
def main (location):
    # Check that the directory exists, otherwise return
    if not os.path.isdir(location):
        print("{location} does not exist or is not a folder.".format(location = location))
        return

    # Work through the directory and any subdirectories, ignoring hidden directories
    print("\nPrimary location: {folder}".format(folder = os.path.join(os.path.abspath(location), "")))
    for path, directories, files in os.walk(location):
        for direct in directories[:]:
            if direct.startswith(".") or direct in var.IGNORE:
                directories.remove(direct)
        print("Current directory: {folder}".format(folder = os.path.join(os.path.abspath(path), "")))
        directories.sort()

        for filename in sorted(files):
            address = os.path.join(path, filename)
            extension = os.path.splitext(filename)[1]

            # Sort all text files that are not blacklisted
            if (extension in var.SECTIONS_EXT) and filename not in var.IGNORE:
                sort.fopsort(address)

            # Delete unnecessary backups and temporary files
            if extension == ".orig" or extension == ".temp":
                try:
                    os.remove(address)
                except(IOError, OSError):
                    # Ignore errors resulting from deleting files, as they likely indicate
                    # that the file has already been deleted
                    pass



def isglobalelement (domains):
    """ Check whether all domains are negations."""
    for domain in domains.split(","):
        if domain and not domain.startswith("~"):
            return False
    return True

if __name__ == '__main__':
    start()
