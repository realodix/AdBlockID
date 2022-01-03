#!/usr/bin/env python3
""" Filter Orderer and Preener

Adjusted for AdBlockID
Based on FOP (RU AdList) v3.921

Copyright (C) 2011 Michael
GNU General Public License
"""

import collections, filecmp, os, re, subprocess, sys
from config import *

def start():
    """ Print a greeting message and run FOP in the directories specified via the command
    line, or the current working directory if no arguments have been passed.
    """

    greeting = "FOP AdBlockID v{version}".format(version = VERSION)
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


def main(location):
    """ Find and sort all the files in a given directory, committing changes to a
    repository if one exists.
    """
    # Check that the directory exists, otherwise return
    if not os.path.isdir(location):
        print("{location} does not exist or is not a folder.".format(location = location))
        return

    # Work through the directory and any subdirectories, ignoring hidden directories
    print("\nPrimary location: {folder}".format(
        folder = os.path.join(os.path.abspath(location), "")))

    for path, directories, files in os.walk(location):
        for direct in directories[:]:
            if direct.startswith(".") or direct in IGNORE:
                directories.remove(direct)

        print("{folder}".format(folder = os.path.join(os.path.abspath(path), "")))
        directories.sort()
        for fileName in sorted(files):
            address = os.path.join(path, fileName)
            extension = os.path.splitext(fileName)[1]

            # Sort all text files that are not blacklisted
            if extension in FILE_EXTENSION and fileName not in IGNORE:
                _FopSort(address)

            # Delete unnecessary backups and temporary files
            if extension == ".orig" or extension == ".temp":
                try:
                    os.remove(address)
                except(IOError, OSError):
                    # Ignore errors resulting from deleting files, as they likely indicate
                    # that the file has already been deleted
                    pass


def _FopSort(fileName):
    """Sort the sections of the file and save any modifications."""

    temporaryFile = "{fileName}.temp".format(fileName = fileName)
    checkLines = 10
    section = []
    linesChecked = 1
    filterLines = elementLines = 0

    # Read in the input and output files concurrently to allow filters to be saved as soon
    # as they are finished with
    with (open(fileName, "r", encoding = "utf-8", newline = "\n") as inputFile,
            open(temporaryFile, "w", encoding = "utf-8", newline = "\n") as outputFile):

        def _CombineFilters(uncombinedFilters, domainPattern, domainSeparator):
            """Combines domains for (further) identical rules."""

            combinedFilters = []

            for i in range(len(uncombinedFilters)):
                domains1 = re.search(domainPattern, uncombinedFilters[i])

                if i+1 < len(uncombinedFilters) and domains1:
                    domains2 = re.search(domainPattern, uncombinedFilters[i+1])
                    domain1str = domains1.group(1)

                if (not domains1
                    or i+1 == len(uncombinedFilters)
                    or not domains2
                    or len(domain1str) == 0
                    or len(domains2.group(1)) == 0):
                    # last filter or filter didn't match regex or no domains
                    combinedFilters.append(uncombinedFilters[i])
                else:
                    domain2str = domains2.group(1)

                    if domains1.group(0).replace(
                        domain1str, domain2str, 1) != domains2.group(0):
                        # non-identical filters shouldn't be combined
                        combinedFilters.append(uncombinedFilters[i])

                    elif (re.sub(domainPattern, "", uncombinedFilters[i])
                        == re.sub(domainPattern, "", uncombinedFilters[i+1])):

                        # identical filters. Try to combine them...
                        newDomains = "{d1}{sep}{d2}".format(
                            d1=domain1str, sep=domainSeparator, d2=domain2str)
                        newDomains = domainSeparator.join(
                            sorted(set(newDomains.split(domainSeparator)),
                                key = lambda domain: domain.strip("~"))
                        )

                        if ((domain1str.count("~") != domain1str.count(domainSeparator) + 1)
                            != (domain2str.count("~") != domain2str.count(domainSeparator) + 1)):
                            # do not combine rules containing included domains with rules
                            # containing only excluded domains
                            combinedFilters.append(uncombinedFilters[i])
                        else:
                            # either both contain one or more included domains, or both
                            # contain only excluded domains
                            domainsSubstitute = domains1.group(0).replace(domain1str, newDomains, 1)
                            uncombinedFilters[i+1] = re.sub(
                                domainPattern, domainsSubstitute, uncombinedFilters[i])
                    else:
                        # non-identical filters shouldn't be combined
                        combinedFilters.append(uncombinedFilters[i])

            return combinedFilters

        def _WriteFilters():
            """Writes the filter lines to the file"""

            if elementLines > filterLines:
                uncombinedFilters = sorted(
                    set(section),
                    key = lambda rule: re.sub(RE_ELEMENTDOMAIN, "", rule)
                )
                outputFile.write(
                    "{filters}\n".format(
                        filters = "\n".join(
                            _CombineFilters(uncombinedFilters, RE_ELEMENTDOMAIN, ","))
                    )
                )
            else:
                uncombinedFilters = sorted(set(section), key = str.lower)
                outputFile.write(
                    "{filters}\n".format(
                        filters = "\n".join(
                            _CombineFilters(uncombinedFilters, RE_FILTERDOMAIN, "|"))
                    )
                )

        for line in inputFile:
            line = line.strip()

            if re.match(RE_BLANKLINE, line):
                continue

            # Include comments verbatim and, if applicable, sort the preceding section of
            # filters and save them in the new version of the file
            if (line[0] == "!" or line[:8] == "%include"
                    or line[0] == "[" and line[-1] == "]"):
                if section:
                    _WriteFilters()
                    section = []
                    linesChecked = 1
                    filterLines = elementLines = 0
                outputFile.write("{line}\n".format(line = line))
            else:
                # Neaten up filters and, if necessary, check their type for the sorting
                # algorithm
                elementParts = re.match(RE_ELEMENT, line)

                if elementParts:
                    domains = elementParts.group(1).lower()

                    if linesChecked <= checkLines:
                        elementLines += 1
                        linesChecked += 1

                    line = _ElementTidy(domains, elementParts.group(2), elementParts.group(3))
                else:
                    if linesChecked <= checkLines:
                        filterLines += 1
                        linesChecked += 1

                    line = _FilterTidy(line)

                # Add the filter to the section
                section.append(line)

        # At the end of the file, sort and save any remaining filters
        if section:
            _WriteFilters()

    # Replace the existing file with the new one only if alterations have been made
    if not filecmp.cmp(temporaryFile, fileName):
        # Check the operating system and, if it is Windows, delete the old file to avoid
        # an exception (it is not possible to rename files to names already in use on
        # this operating system)
        if os.name == "nt":
            os.remove(fileName)

        os.rename(temporaryFile, fileName)
        print("Sorted: {fileName}".format(fileName = os.path.basename(fileName)))
    else:
        os.remove(temporaryFile)


def _SortFunc(option):
    # For identical options, the inverse always follows the non-inverse option ($image,
    # ~image instead of $~image,image) with exception for popup filter
    if option[0] == "~":
        return option[1:] + "{"
    if option == "popup":
        return option + "}"

    # Also will always be first in the list
    if (option.find("important") > -1 or option.find("first-party") > -1
            or option.find("strict1p") > -1 or option.find("third-party") > -1
            or option.find("strict3p") > -1):
        return "0" + option

    # And let badfilter and key=value parameters will always be last in the list
    if option.find("badfilter") > -1:
        return "|" + option
    if option.split('=')[0] in KNOWNPARAMETERS:
        return "}" + option

    return option


def _FilterTidy(filterin):
    """ Sort the options of blocking filters and make the filter text lower case if
    applicable.
    """

    optionSplit = re.match(RE_OPTION, filterin)

    if not optionSplit:
        # Remove unnecessary asterisks from filters without any options and return them
        return _RemoveUnnecessaryWildcards(filterin, False)
    else:
        # If applicable, separate and sort the filter options in addition to the filter
        # text
        optionList = optionSplit.group(2).lower().split(",")

        domainList = []
        denyAllow = []
        rediwriteList = []
        removeParam = ""
        removeEntries = []
        keepAsterisk = False

        for option in optionList:
            # Detect and separate domain options
            if option[0:7] == "domain=":
                domainList.extend(option[7:].split("|"))
                removeEntries.append(option)
            elif option[0:10] == "denyallow=":
                if "domain=" not in filterin:
                    print("Warning: \"denyallow=\" option requires the \"domain=\" option."
                        "\n \"{}\"".format(filterin))
                denyAllow.extend(option[10:].split("|"))
                removeEntries.append(option)
            elif option[0:12] == "removeparam=":
                removeParam = option[12:]
                removeEntries.append(option)
            elif re.match(RE_OPTION_REDIRECT, option):
                keepAsterisk = True
                rediwriteList.append(option)
            elif option == "popunder":
                keepAsterisk = True
            elif (option.strip("~") not in KNOWNOPTIONS
                and option.split('=')[0] not in KNOWNPARAMETERS):

                print("Warning: The option \"{option}\" used on the filter"
                    "\"{problemfilter}\" is not recognised by FOP".format(
                        option = option, problemfilter = filterin))

        # Sort all options other than domain alphabetically with a few exceptions
        optionList = sorted(
            set(filter(lambda option: (option not in removeEntries)
                and (option not in rediwriteList),
                optionList
            )),
            key = _SortFunc
        )

        # Replace underscore typo with hyphen-minus in options like third_party
        optionList = list(map(lambda option: option.replace("_", "-"), optionList))

        # Append `removeparam` back at the end (both to keep it at the end and skip
        # underscore typo fix)
        if removeParam:
            optionList.append("removeparam={}".format(removeParam))

        # Append redirect rule back without underscore typo fix
        if rediwriteList:
            optionList.extend(rediwriteList)

        # If applicable, sort domain restrictions and append them to the list of options
        if denyAllow:
            optionList.append(
                "denyallow={denyAllow}".format(
                    denyAllow = "|".join(sorted(set(denyAllow))).lstrip('|'))
            )
        if domainList:
            optionList.append(
                "domain={domainList}".format(
                    domainList = "|".join(sorted(set(domainList),
                    key = lambda domain: domain.strip("~"))).lstrip('|'))
            )

        # according to uBO documentation redirect options must start either with * or ||
        # so, it is not unnecessary wildcard in such case
        filterText = _RemoveUnnecessaryWildcards(optionSplit.group(1), keepAsterisk)
        if (keepAsterisk
                and (len(filterText) < 1
                    or (len(filterText) > 0
                        and filterText[0] != '*'
                        and filterText[:2] != '||'
            ))):

            print("Warning: Incorrect filter \"{filterin}\". Such filters must start with"
                "either '*' or '||'.".format(filterin = filterin))

        # Return the full filter
        return ("{filterText}${options}".format(
            filterText = filterText, options = ",".join(optionList)))


def _ElementTidy(domains, separator, selector):
    """ Sort the domains of element hiding rules, remove unnecessary tags and make the
    relevant sections of the rule lower case.
    """

    # Order domain names alphabetically, ignoring exceptions
    if "," in domains:
        domains = (
            ","
            .join(sorted(set(domains.split(",")), key = lambda domain: domain.strip("~")))
            .lstrip(',')
        )

    # Skip non-selectors (uBO's JS injections and other)
    if re.match(RE_NONSELECTOR, selector) != None:
        return ("{domain}{separator}{selector}".format(
            domain = domains, separator = separator, selector = selector))

    # Mark the beginning and end of the selector with "@"
    selectorAndTail = re.match(RE_SELECTORANDTAIL, selector) #selector.split(':style(')
    splitterPart = ""
    tailPart = ""

    if selectorAndTail.group(2) != None:
        splitterPart = selectorAndTail.group(3)
        tailPart = selectorAndTail.group(4)

    selector = "@{selector}@".format(selector = selectorAndTail.group(1))
    each = re.finditer
    # Make sure we don't match items in strings (e.g., don't touch Width in
    # ##[style="height:1px; Width: 123px;"])
    selectorWithoutStrings = selector
    selectorOnlyStrings = ""

    while True:
        stringMatch = re.match(RE_ATTRIBUTEVALUE, selectorWithoutStrings)

        if stringMatch == None:
            break

        selectorWithoutStrings = selectorWithoutStrings.replace(
            "{before}{stringPart}".format(
                before = stringMatch.group(1), stringPart = stringMatch.group(2)),
            "{before}".format(before = stringMatch.group(1)),
            1
        )
        selectorOnlyStrings = "{old}{new}".format(
            old = selectorOnlyStrings, new = stringMatch.group(2))

    # Clean up tree selectors
    for tree in each(RE_TREESELECTOR, selector):

        if (tree.group(0) in selectorOnlyStrings
                or not tree.group(0) in selectorWithoutStrings):
            continue

        # added check for case when tree selector were used in :-abp-has() and similar
        # constructions at first position. Basically for cases like PARENT:-abp-has(> CHILD)
        replaceBy = ("{sp}{g2} ".format(
            sp = ("" if tree.group(1) == "(" else " "), g2 = tree.group(2)))
        if replaceBy == "   ":
            replaceBy = " "
        selector = selector.replace(
            tree.group(0),
            "{g1}{replaceBy}{g3}".format(
                g1 = tree.group(1), replaceBy = replaceBy, g3 = tree.group(3)),
            1
        )

    # Remove unnecessary tags
    for untag in each(RE_REMOVE_AST, selector):
        untagName = untag.group(4)
        if untagName in selectorOnlyStrings or not untagName in selectorWithoutStrings:
            continue

        bc = untag.group(2)
        if bc == None:
            bc = untag.group(3)

        ac = untag.group(5)

        selector = selector.replace(
            "{before}{untag}{after}".format(before = bc, untag = untagName, after = ac),
            "{before}{after}".format(before = bc, after = ac),
            1
        )

    # Make the remaining tags lower case wherever possible
    for tag in each(RE_SELECTOR, selector):
        tagName = tag.group(1)
        if tagName in selectorOnlyStrings or not tagName in selectorWithoutStrings:
            continue

        if re.search(RE_UNICODESELECTOR, selectorWithoutStrings) != None: break

        ac = tag.group(3)
        if ac == None:
            ac = tag.group(4)

        selector = selector.replace(
            "{tag}{after}".format(tag = tagName, after = ac),
            "{tag}{after}".format(tag = tagName.lower(), after = ac),
            1
        )

    # Make pseudo classes lower case where possible
    for pseudo in each(RE_PSEUDO, selector):
        pseudoClass = pseudo.group(1)

        if (pseudoClass in selectorOnlyStrings
                or not pseudoClass in selectorWithoutStrings):
            continue

        ac = pseudo.group(2)
        selector = selector.replace(
            "{pClass}{after}".format(pClass = pseudoClass, after = ac),
            "{pClass}{after}".format(pClass = pseudoClass.lower(), after = ac),
            1
        )

    # Remove unnecessary 'px' in '0px' and space in "! important"
    if splitterPart == ":style" or splitterPart == ":matches-css" and tailPart != None:
        for un0px in each(RE_REMOVE_0PX, tailPart):
            bc = un0px.group(2)
            ac = un0px.group(4)
            tailPart = tailPart.replace(
                "{before}{remove}{after}".format(
                    before = bc, remove = un0px.group(3), after = ac),
                "{before}{after}".format(before = bc, after = ac),
                1
            )

        for bsi in each(RE_BANGSPACEIMPORTANT, tailPart):
            bc = bsi.group(1)
            space = "" if bc == " " else " "
            ac = bsi.group(3)
            tailPart = tailPart.replace(
                "{before}{bang}{after}".format(
                    before = bc, bang = bsi.group(2), after = ac),
                "{before}{space}!{after}".format(before = bc, space = space, after = ac),
                1
            )

    # Remove the markers from the beginning and end of the selector and return the
    # complete rule
    return ("{domain}{separator}{selector}{splitter}{tail}".format(
        domain = domains,
        separator = separator,
        selector = selector[1:-1],
        splitter = splitterPart,
        tail = tailPart)
    )


def _IsGlobalElement(domains):
    """Check whether all domains are negations."""

    for domain in domains.split(","):
        if domain and not domain.startswith("~"):
            return False

    return True


def _RemoveUnnecessaryWildcards(filterText, keepAsterisk):
    """ Where possible, remove unnecessary wildcards from the beginnings and ends of
    blocking filters.
    """

    allowList = False
    hadStar = False

    if filterText[0:2] == "@@":
        allowList = True
        filterText = filterText[2:]

    while (len(filterText) > 1
            and filterText[0] == "*"
            and not filterText[1] == "|"
            and not filterText[1] == "!"):
        filterText = filterText[1:]
        hadStar = True

    while (len(filterText) > 1
            and filterText[-1] == "*"
            and not filterText[-2] == "|"
            and not filterText[-2] == " "):
        filterText = filterText[:-1]
        hadStar = True

    if hadStar and filterText[0] == "/" and filterText[-1] == "/":
        filterText = "{filterText}*".format(filterText = filterText)

    if hadStar and keepAsterisk:
        filterText = "*{filterText}".format(filterText = filterText)

    if not keepAsterisk and filterText == "*":
        filterText = ""

    if allowList:
        filterText = "@@{filterText}".format(filterText = filterText)

    return filterText


if __name__ == '__main__':
    start()
