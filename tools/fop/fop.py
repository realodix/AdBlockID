#!/usr/bin/env python3

""" FOP_FH
    Filter Orderer and Preener (tweaked by Realodix)
    Copyright (C) 2011 Michael

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>."""
# Import the key modules
import re, os, sys, filecmp, argparse

# FOP version number
VERSION = "1.12"

# Welcome message
greeting = f"FOP (Filter Orderer and Preener) v{VERSION}"

ap = argparse.ArgumentParser()
ap.add_argument('--dir', '-d', nargs='+', help='Set directories', default=None)
ap.add_argument('--ignore', '-i', nargs='+', help='List the files that should not be sorted, either because they have a special sorting system or because they are not filter files', default=("dist", "requirements.txt", "templates", "node_modules"))
ap.add_argument("--version", "-v",
                action='store_true', help="Show script's version number and exit")

FILE_EXTENSION = [".adfl", ".txt"]

# Compile regular expressions to match important filter parts
# (derived from Wladimir Palant's Adblock Plus source code)
ELEMENTDOMAINPATTERN = re.compile(r"^([^\/\*\|\@\"\!]*?)(#|\$)\@?\??\@?(#|\$)")
FILTERDOMAINPATTERN = re.compile(r"(?:\$|\,)(?:domain|from)\=([^\,\s]+)$")
ELEMENTPATTERN = re.compile(
    r"^([^\/\*\|\@\"\!]*?)(\$\@?\$|##\@?\$|#[\@\?]?#\+?)(.*)$")
OPTIONPATTERN = re.compile(
    r"^(.*)\$(~?[\w\-]+(?:=[^,\s]+)?(?:,~?[\w\-]+(?:=[^,\s]+)?)*)$")
RE_OPTION_REDIRECT = re.compile(r"""
    ^(.+)?
    (redirect(-rule)?)=
    (
        1x1.gif|(2x2|3x2|32x32).png
        |noop-0.1s.mp3|noop-0.5s.mp3|noop-1s.mp4
        |noop.html|noop.js|noop.txt|noopcss
        |ampproject_v0.js|nofab.js|fuckadblock.js-3.2.0
        |google-analytics_(cx_api.js|analytics.js|ga.js)
        |googlesyndication_adsbygoogle.js|googletagmanager_gtm.js|googletagservices_gpt.js
        |click2load.html
    )
    (,.+)?$
""", re.X)
# Compile regular expressions that match element tags and
# pseudo classes and strings and tree selectors;
# "@" indicates either the beginning or the end of a selector
SELECTORPATTERN = re.compile(
    r"(?<=[\s\[@])([a-zA-Z]*[A-Z][a-zA-Z0-9]*)((?=([\[\]\^\*\$=:@#\.]))|(?=(\s(?:[+>~]|\*|[a-zA-Z][a-zA-Z0-9]*[\[:@\s#\.]|[#\.][a-zA-Z][a-zA-Z0-9]*))))")
PSEUDOPATTERN = re.compile(
    r"(\:[:][a-zA-Z\-]*[A-Z][a-zA-Z\-]*)(?=([\(\:\@\s]))")
REMOVALPATTERN = re.compile(
    r"((?<=([>+~,]\s))|(?<=(@|\s|,)))()(?=(?:[#\.\[]|\:(?!-abp-)))")
ATTRIBUTEVALUEPATTERN = re.compile(
    r"^([^\'\"\\]|\\.)*(\"(?:[^\"\\]|\\.)*\"|\'(?:[^\'\\]|\\.)*\')|\*")
TREESELECTORPATTERN = re.compile(r"(\\.|[^\+\>\~\\\ \t])\s*([\+\>\~\ \t])\s*(\D)")
# UNICODESELECTOR = re.compile(r"\\[0-9a-fA-F]{1,6}\s[a-zA-Z]*[A-Z]")

# Compile a regular expression that describes a completely blank line
BLANKPATTERN = re.compile(r"^\s*$")

# Compile a regular expression that describes uBO's scriptlets pattern
UBO_JS_PATTERN = re.compile(r"^@js\(")

# List all uBlock Origin (excepting: domain, removeparam, denyallow, from, method; which is handled separately)
KNOWNOPTIONS = (
    '_', 'all', 'badfilter', 'important', 'other', 'empty',
    '1p', 'first-party', 'strict1p', '3p', 'third-party', 'strict3p',
    'cname', 'css', 'stylesheet', 'csp', 'doc', 'document', 'domain', 'ehide', 'elemhide',
    'font', 'frame', 'generichide','ghide', 'header', 'image', 'inline-font',
    'inline-script', 'match-case', 'media', 'mp4', 'object', 'ping', 'popunder',
    'popup', 'script', 'shide', 'specifichide', 'subdocument', 'to', 'websocket', 'xhr',
    'xmlhttprequest'
)


def start():
    """ Print a greeting message and run FOP in the directories
    specified via the command line, or the current working directory if
    no arguments have been passed."""
    if arg.version:
        print(greeting)
        sys.exit(0)
    characters = len(str(greeting))
    print("=" * characters)
    print(greeting)
    print("=" * characters)

    # Convert the directory names to absolute references and visit each unique location
    places = arg.dir
    if places:
        places = [os.path.abspath(place) for place in places]
        for place in sorted(set(places)):
            main(place)
            print()
    else:
        main(os.getcwd())


def main(location):
    """ Find and sort all the files in a given directory."""
    # Check that the directory exists, otherwise return
    if not os.path.isdir(location):
        print(f"{location} does not exist or is not a folder.")
        return

    # Work through the directory and any subdirectories, ignoring hidden directories
    print(f'\nPrimary location: {os.path.join(os.path.abspath(location), "")}')
    for path, directories, files in os.walk(location):
        for direct in directories[:]:
            if direct.startswith(".") or direct in arg.ignore:
                directories.remove(direct)
        print(f'Current directory - {os.path.join(os.path.abspath(path), "")}')
        directories.sort()
        for filename in sorted(files):
            address = os.path.join(path, filename)
            extension = os.path.splitext(filename)[1]
            # Sort all text files that are not blacklisted
            if extension in FILE_EXTENSION and filename not in arg.ignore:
                fopsort(address)
            # Delete unnecessary backups and temporary files
            if extension in (".orig", ".temp"):
                try:
                    os.remove(address)
                except(IOError, OSError):
                    # Ignore errors resulting from deleting files, as they likely indicate that the file has already been deleted
                    pass


def fopsort(filename):
    """ Sort the sections of the file and save any modifications."""
    temporaryfile = f"{filename}.temp"
    check_lines = 10
    section = []
    lineschecked = 1
    filterlines = elementlines = 0

    # Read in the input and output files concurrently to allow filters to be saved as soon as they are finished with
    with open(filename, "r", encoding="utf-8", newline="\n") as inputfile, open(temporaryfile, "w", encoding="utf-8", newline="\n") as outputfile:

        # Combines domains for (further) identical rules
        def combinefilters(uncombinedFilters, DOMAINPATTERN, domainseparator):
            combinedFilters = []
            for i, uncombinedFilter in enumerate(uncombinedFilters):
                domains1 = re.search(DOMAINPATTERN, uncombinedFilter)
                if i+1 < len(uncombinedFilters) and domains1:
                    domains2 = re.search(DOMAINPATTERN, uncombinedFilters[i+1])
                    domain1str = domains1.group(1)

                if not domains1 or i+1 == len(uncombinedFilters) or not domains2 or len(domain1str) == 0 or len(domains2.group(1)) == 0:
                    # last filter or filter didn't match regex or no domains
                    combinedFilters.append(uncombinedFilter)
                else:
                    domain2str = domains2.group(1)
                    if domains1.group(0).replace(domain1str, domain2str, 1) != domains2.group(0):
                        # non-identical filters shouldn't be combined
                        combinedFilters.append(uncombinedFilter)
                    elif re.sub(DOMAINPATTERN, "", uncombinedFilter) == re.sub(DOMAINPATTERN, "", uncombinedFilters[i+1]):
                        # identical filters. Try to combine them...
                        newDomains = f"{domain1str}{domainseparator}{domain2str}"
                        newDomains = domainseparator.join(sorted(
                            set(newDomains.split(domainseparator)), key=lambda domain: domain.strip("~")))
                        if (domain1str.count("~") != domain1str.count(domainseparator) + 1) != (domain2str.count("~") != domain2str.count(domainseparator) + 1):
                            # do not combine rules containing included domains with rules containing only excluded domains
                            combinedFilters.append(uncombinedFilter)
                        else:
                            # either both contain one or more included domains, or both contain only excluded domains
                            domainssubstitute = domains1.group(
                                0).replace(domain1str, newDomains, 1)
                            uncombinedFilters[i+1] = re.sub(
                                DOMAINPATTERN, domainssubstitute, uncombinedFilter)
                    else:
                        # non-identical filters shouldn't be combined
                        combinedFilters.append(uncombinedFilter)
            return combinedFilters

        # Writes the filter lines to the file
        def writefilters():
            if elementlines > filterlines:
                uncombinedFilters = sorted(
                    set(section), key=lambda rule: re.sub(ELEMENTDOMAINPATTERN, "", rule))
                outputfile.write("{filters}\n".format(filters="\n".join(
                    combinefilters(uncombinedFilters, ELEMENTDOMAINPATTERN, ","))))
            else:
                uncombinedFilters = sorted(set(section), key=str.lower)
                outputfile.write("{filters}\n".format(filters="\n".join(
                    combinefilters(uncombinedFilters, FILTERDOMAINPATTERN, "|"))))

        for line in inputfile:
            line = line.strip()
            if not re.match(BLANKPATTERN, line):
                # Include comments verbatim and, if applicable, sort the preceding section of filters and save them in the new version of the file
                if line[0] == "!" or line[:8] == "%include" or line[0] == "[" and line[-1] == "]":
                    if section:
                        writefilters()
                        section = []
                        lineschecked = 1
                        filterlines = elementlines = 0
                    outputfile.write(f"{line}\n")
                else:
                    # Neaten up filters and, if necessary, check their type for the sorting algorithm
                    elementparts = re.match(ELEMENTPATTERN, line)
                    if elementparts:
                        domains = elementparts.group(1).lower()
                        if lineschecked <= check_lines:
                            elementlines += 1
                            lineschecked += 1
                        line = elementtidy(domains, elementparts.group(
                            2), elementparts.group(3))
                    else:
                        if lineschecked <= check_lines:
                            filterlines += 1
                            lineschecked += 1
                        line = filtertidy(line, filename)
                    # Add the filter to the section
                    section.append(line)
        # At the end of the file, sort and save any remaining filters
        if section:
            writefilters()

    # Replace the existing file with the new one only if alterations have been made
    if not filecmp.cmp(temporaryfile, filename):
        os.replace(temporaryfile, filename)
        head, tail = os.path.split(filename)
        print(f"- Sorted: {tail}")
    else:
        os.remove(temporaryfile)


def filtertidy(filterin, filename):
    """ Sort the options of blocking filters and make the filter text
    lower case if applicable."""
    optionsplit = re.match(OPTIONPATTERN, filterin)

    if not optionsplit:
        # Remove unnecessary asterisks from filters without any options and return them
        return removeunnecessarywildcards(filterin)

    # If applicable, separate and sort the filter options in addition to the filter text
    filtertext = removeunnecessarywildcards(optionsplit.group(1))
    optionlist = optionsplit.group(2).lower().split(",")

    domainlist = []
    fromlist = []
    to_list = []
    denyallowlist = []
    redirectlist = []
    removeentries = []
    # Get line number of the filter in the file
    linenumber = ""
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if line.strip() == filterin:
                linenumber = f"{i+1}"
                break

    for option in optionlist:
        # Detect and separate domain options
        if option[0:7] == "domain=":
            domainlist.extend(option[7:].split("|"))
            removeentries.append(option)
        elif option[0:5] == "from=":
            fromlist.extend(option[5:].split("|"))
            removeentries.append(option)
        elif option[0:10] == "denyallow=":
            if "domain=" not in filterin:
                m = f'\n- \"denyallow=\" option requires the \"domain=\" option.\n'\
                    f'  {filename}:{linenumber}\n\n'\
                    f'  {filterin}'\
                    f' \n'
                print(m)
            denyallowlist.extend(option[10:].split("|"))
            removeentries.append(option)
        elif option[0:3] == "to=":
            if "from=" not in filterin:
                m = f'\n- \"to=\" option requires the \"domain=\" option.\n'\
                    f'  {filename}:{linenumber}\n\n'\
                    f'  {filterin}'\
                    f' \n'
                print(m)
            to_list.extend(option[3:].split("|"))
            removeentries.append(option)
        elif re.match(RE_OPTION_REDIRECT, option):
            redirectlist.append(option)
        elif "removeparam=" == option[0:12] or "method" == option[0:6]:
            optionlist = optionsplit.group(2).split(",")
        elif option.strip("~") not in KNOWNOPTIONS:
            m = f'- The option \"{option}\" is not recognised by FOP\n'\
                f'  {filename}:{linenumber}\n\n'\
                f'  {filterin}'\
                f' \n'
            print(m)

    # Sort all options other than domain alphabetically
    # For identical options, the inverse always follows the non-inverse option ($image,~image instead of $~image,image)
    optionlist = sorted(
        set(filter(lambda option: (option not in removeentries) and (option not in redirectlist), optionlist)),
        key=sortfunc
    )
    # If applicable, sort redirect and rewrite options and append them to the list of options
    if redirectlist:
        optionlist.extend(redirectlist)
    # If applicable, sort domain restrictions and append them to the list of options
    if domainlist:
        optionlist.append(
            f'domain={"|".join(sorted(set(filter(lambda domain: domain != "", domainlist)), key=lambda domain: domain.strip("~")))}')
    if fromlist:
        optionlist.append(
            f'from={"|".join(sorted(set(filter(lambda domain: domain != "", fromlist)), key=lambda domain: domain.strip("~")))}')
    # If applicable, sort denyallow options and append them to the list of options
    if denyallowlist:
        optionlist.append(
            f'denyallow={"|".join(sorted(set(filter(lambda domain: domain != "", denyallowlist)), key=lambda domain: domain.strip("~")))}')
    if to_list:
        optionlist.append(
            f'to={"|".join(sorted(set(filter(lambda domain: domain != "", to_list)), key=lambda domain: domain.strip("~")))}')

    # Return the full filter
    return f'{filtertext}${",".join(optionlist)}'


def sortfunc (option):
    # For identical options, the inverse always follows the non-inverse option
    # (e.g., $image,~image instead of $~image,image)
    if option[0] == "~": return option[1:] + "~"

    # Also will always be first in the list
    if (option.find("important") > -1
       or option.find("first-party") > -1
       or option.find("strict1p") > -1
       or option.find("third-party") > -1
       or option.find("strict3p") > -1):
        return "0" + option

    # let badfilter will always be last in the list
    if option.find("badfilter") > -1: return "|" + option

    # move the `_` option to the position after the `removeparam` option
    if option.find("removeparam") > -1: return "1" + option
    if option.find("_") > -1: return "2" + option


    return option

def elementtidy(domains, separator, selector):
    """ Sort the domains of element hiding rules, remove unnecessary
    tags and make the relevant sections of the rule lower case."""
    # Order domain names alphabetically, ignoring exceptions
    if "," in domains:
        domains = ",".join(sorted(set(domains.split(",")),
                           key=lambda domain: domain.strip("~")))
    # Mark the beginning and end of the selector with "@"
    selector = f"@{selector}@"
    each = re.finditer
    # Make sure we don't match items in strings (e.g., don't touch Width in ##[style="height:1px; Width: 123px;"])
    selectorwithoutstrings = selector
    selectoronlystrings = ""
    while True:
        stringmatch = re.match(ATTRIBUTEVALUEPATTERN, selectorwithoutstrings)
        if stringmatch is None:
            break
        selectorwithoutstrings = selectorwithoutstrings.replace(
            f"{stringmatch.group(1)}{stringmatch.group(2)}", f"{stringmatch.group(1)}", 1)
        selectoronlystrings = f"{selectoronlystrings}{stringmatch.group(2)}"

    # Clean up tree selectors
    for tree in each(TREESELECTORPATTERN, selector):
        if tree.group(0) in selectoronlystrings or not tree.group(0) in selectorwithoutstrings:
            continue
        if tree.group(1) == "(":
            replaceby = f"{tree.group(2)} "
        else:
            replaceby = f" {tree.group(2)} "
        if replaceby == "   ":
            replaceby = " "
        # Make sure we don't match arguments of uBO scriptlets
        if not UBO_JS_PATTERN.match(selector):
            selector = selector.replace(tree.group(
                0), f"{tree.group(1)}{replaceby}{tree.group(3)}", 1)
    # Remove unnecessary tags
    for untag in each(REMOVALPATTERN, selector):
        untagname = untag.group(4)
        if untagname in selectoronlystrings or not untagname in selectorwithoutstrings:
            continue
        bc = untag.group(2)
        if bc is None:
            bc = untag.group(3)
        ac = untag.group(5)
        selector = selector.replace(f"{bc}{untagname}{ac}", f"{bc}{ac}", 1)
    # Make pseudo classes lower case where possible
    for pseudo in each(PSEUDOPATTERN, selector):
        pseudoclass = pseudo.group(1)
        if pseudoclass in selectoronlystrings or not pseudoclass in selectorwithoutstrings:
            continue
        ac = pseudo.group(3)
        selector = selector.replace(
            f"{pseudoclass}{ac}", f"{pseudoclass}{ac}", 1)
    # Remove the markers from the beginning and end of the selector and return the complete rule
    return f"{domains}{separator}{selector[1:-1]}"


def removeunnecessarywildcards(filtertext):
    # Where possible, remove unnecessary wildcards from the beginnings and ends of blocking filters.
    allowlist = False
    hadStar = False
    if filtertext[0:2] == "@@":
        allowlist = True
        filtertext = filtertext[2:]
    while len(filtertext) > 1 and filtertext[0] == "" and not filtertext[1] == "|" and not filtertext[1] == "!":
        filtertext = filtertext[1:]
        hadStar = True
    while len(filtertext) > 1 and filtertext[-1] == "" and not filtertext[-2] == "|":
        filtertext = filtertext[:-1]
        hadStar = True
    if hadStar and filtertext[0] == "/" and filtertext[-1] == "/":
        filtertext = f"{filtertext}*"
    if filtertext == "":
        filtertext = ""
    if allowlist:
        filtertext = f"@@{filtertext}"
    return filtertext


if __name__ == '__main__':
    arg = ap.parse_args()
    start()
