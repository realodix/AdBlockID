import filecmp, os, re
import helper, var


""" Sort the sections of the file and save any modifications."""
def fopsort (filename):
    temporaryfile = "{filename}.temp".format(filename = filename)
    CHECKLINES = 10
    section = []
    lineschecked = 1
    filterlines = elementlines = 0

    # Read in the input and output files concurrently to allow filters to be saved as soon
    # as they are finished with
    with open(filename, "r", encoding = "utf-8", newline = "\n") as inputfile, open(temporaryfile, "w", encoding = "utf-8", newline = "\n") as outputfile:

        # Combines domains for (further) identical rules
        def combinefilters(uncombinedFilters, DOMAINPATTERN, domainseparator):
            combinedFilters = []

            for i in range(len(uncombinedFilters)):
                domains1 = re.search(DOMAINPATTERN, uncombinedFilters[i])

                if i+1 < len(uncombinedFilters) and domains1:
                    domains2 = re.search(DOMAINPATTERN, uncombinedFilters[i+1])
                    domain1str = domains1.group(1)

                if not domains1 or i+1 == len(uncombinedFilters) or not domains2 or len(domain1str) == 0 or len(domains2.group(1)) == 0:
                    # last filter or filter didn't match regex or no domains
                    combinedFilters.append(uncombinedFilters[i])
                else:
                    domain2str = domains2.group(1)

                    if domains1.group(0).replace(domain1str, domain2str, 1) != domains2.group(0):
                        # non-identical filters shouldn't be combined
                        combinedFilters.append(uncombinedFilters[i])
                    elif re.sub(DOMAINPATTERN, "", uncombinedFilters[i]) == re.sub(DOMAINPATTERN, "", uncombinedFilters[i+1]):
                        # identical filters. Try to combine them...
                        newDomains = "{d1}{sep}{d2}".format(d1=domain1str, sep=domainseparator, d2=domain2str)
                        newDomains = domainseparator.join(sorted(set(newDomains.split(domainseparator)), key = lambda domain: domain.strip("~")))

                        if (domain1str.count("~") != domain1str.count(domainseparator) + 1) != (domain2str.count("~") != domain2str.count(domainseparator) + 1):
                            # do not combine rules containing included domains with rules
                            # containing only excluded domains
                            combinedFilters.append(uncombinedFilters[i])
                        else:
                            # either both contain one or more included domains, or both
                            # contain only excluded domains
                            domainssubstitute = domains1.group(0).replace(domain1str, newDomains, 1)
                            uncombinedFilters[i+1] = re.sub(DOMAINPATTERN, domainssubstitute, uncombinedFilters[i])
                    else:
                        # non-identical filters shouldn't be combined
                        combinedFilters.append(uncombinedFilters[i])
            return combinedFilters

        # Writes the filter lines to the file
        def writefilters():
            if elementlines > filterlines:
                uncombinedFilters = sorted(set(section), key = lambda rule: re.sub(var.ELEMENTDOMAINPATTERN, "", rule))
                outputfile.write("{filters}\n".format(filters = "\n".join(combinefilters(uncombinedFilters, var.ELEMENTDOMAINPATTERN, ","))))
            else:
                uncombinedFilters = sorted(set(section), key = str.lower)
                outputfile.write("{filters}\n".format(filters = "\n".join(combinefilters(uncombinedFilters, var.FILTERDOMAINPATTERN, "|"))))

        for line in inputfile:
            line = line.strip()

            if re.match(var.BLANKPATTERN, line):
                continue

            # Include comments verbatim and, if applicable, sort the preceding section of
            # filters and save them in the new version of the file
            if line[0] == "!" or line[:8] == "%include" or line[0] == "[" and line[-1] == "]":
                if section:
                    writefilters()
                    section = []
                    lineschecked = 1
                    filterlines = elementlines = 0
                outputfile.write("{line}\n".format(line = line))
            else:
                # Neaten up filters and, if necessary, check their type for the sorting
                # algorithm
                elementparts = re.match(var.ELEMENTPATTERN, line)
                if elementparts:
                    domains = elementparts.group(1).lower()
                    if lineschecked <= CHECKLINES:
                        elementlines += 1
                        lineschecked += 1
                    line = helper.elementtidy(domains, elementparts.group(2), elementparts.group(3))
                else:
                    if lineschecked <= CHECKLINES:
                        filterlines += 1
                        lineschecked += 1
                    line = helper.filtertidy(line)
                # Add the filter to the section
                section.append(line)

        # At the end of the file, sort and save any remaining filters
        if section:
            writefilters()

    # Replace the existing file with the new one only if alterations have been made
    if not filecmp.cmp(temporaryfile, filename):
        # Check the operating system and, if it is Windows, delete the old file to avoid
        # an exception (it is not possible to rename files to names already in use on
        # this operating system)
        if os.name == "nt":
            os.remove(filename)
        os.rename(temporaryfile, filename)
        print("Sorted: {filename}".format(filename = os.path.abspath(filename)))
    else:
        os.remove(temporaryfile)


def sortfunc (option):
    # For identical options, the inverse always follows the non-inverse option ($image,
    # ~image instead of $~image,image) with exception for popup filter
    if option[0] == "~": return option[1:] + "{"

    if option == "popup": return option + "}"

    # Also let third-party will always be first in the list
    if option.find("third-party") > -1: return "0" + option

    # And let badfilter and key=value parameters will always be last in the list
    if option.find("badfilter") > -1: return "|" + option

    if option.split('=')[0] in var.KNOWNPARAMETERS: return "}" + option

    return option
