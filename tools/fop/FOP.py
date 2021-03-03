#!/usr/bin/env python3

# FOP version number
VERSION = 3.921

# Import the key modules
import collections, filecmp, os, re, subprocess, sys

# Check the version of Python for language compatibility and subprocess.check_output()
MAJORREQUIRED = 3
MINORREQUIRED = 1
if sys.version_info < (MAJORREQUIRED, MINORREQUIRED):
    raise RuntimeError("FOP requires Python {reqmajor}.{reqminor} or greater, but Python {ismajor}.{isminor} is being used to run this program.".format(reqmajor = MAJORREQUIRED, reqminor = MINORREQUIRED, ismajor = sys.version_info.major, isminor = sys.version_info.minor))

# Import a module only available in Python 3
from urllib.parse import urlparse

# Compile regular expressions to match important filter parts (derived from Wladimir Palant's Adblock Plus source code)
ELEMENTDOMAINPATTERN = re.compile(r"^([^\/\*\|\@\"\!]*?)#[@$?]?#")
FILTERDOMAINPATTERN = re.compile(r"(?:\$|\,)domain\=([^\,\s]+)$")
ELEMENTPATTERN = re.compile(r"^([^\/\*\|\@\"\!]*?)(#[@$?]?#)([^{}]+)$")
OPTIONPATTERN = re.compile(r"^(.*)\$(~?[\w\-]+(?:=[^,\s]+)?(?:,~?[\w\-]+(?:=[^,\s]+)?)*)$")
REDIWRITEOPTIONPATTERN = re.compile(r"^(redirect(-rule)?|rewrite)=")

# Compile regular expressions that match element tags and pseudo classes and strings and tree selectors; "@" indicates either the beginning or the end of a selector
SELECTORPATTERN = re.compile(r"(?<=[\s\[@])([a-zA-Z]*[A-Z][a-zA-Z0-9]*)((?=([\[\]\^\*\$=:@#\.]))|(?=(\s(?:[+>~]|\*|[a-zA-Z][a-zA-Z0-9]*[\[:@\s#\.]|[#\.][a-zA-Z][a-zA-Z0-9]*))))")
PSEUDOPATTERN = re.compile(r"(\:[a-zA-Z\-]*[A-Z][a-zA-Z\-]*)(?=([\(\:\@\s]))")
# (?!:-) - skip Adblock Plus' :-abp-... pseudoclasses, (?!:style\() - skip uBlock Origin's :style() pseudoclass
REMOVE_AST_PATTERN = re.compile(r"((?<=([>+~,]\s))|(?<=(@|\s|,)))(\*)(?=([#\.\[\:]))(?!:-)(?!:style\()")
SELECTORSTYLEPART = re.compile(r":style\(.+\)$")
REMOVE_0PX_PATTERN = re.compile(r"((?<=([\:\s]0))(px)(?=([\s\!])))")
BANGSPACEIMPORTANT = re.compile(r"(.)(\!\s)(important)")
ATTRIBUTEVALUEPATTERN = re.compile(r"^([^\'\"\\]|\\.)*(\"(?:[^\"\\]|\\.)*\"|\'(?:[^\'\\]|\\.)*\')")
TREESELECTOR = re.compile(r"(\\.|[^\+\>\~\\\ \t])\s*([\+\>\~\ \t])\s*(\D)")
UNICODESELECTOR = re.compile(r"\\[0-9a-fA-F]{1,6}\s[a-zA-Z]*[A-Z]")
NONSELECTOR = re.compile(r"^(\+js\(|script:inject\()")
SELECTORANDTAILPATTERN = re.compile(r"^(.*?)((:-abp-contains|:style)(.*))?$")

# Compile a regular expression that describes a completely blank line
BLANKPATTERN = re.compile(r"^\s*$")

# Compile a regular expression that validates commit comments
COMMITPATTERN = re.compile(r"^(A|M|P)\:\s(\((.+)\)\s)?(.*)$")

# List the files that should not be sorted, either because they have a special sorting system or because they are not filter files
IGNORE = ("CC-BY-SA.txt", "easytest.txt", "GPL.txt", "MPL.txt", "antinuha.txt",
          "enhancedstats-addon.txt", "fanboy-tracking", "firefox-regional", "other")

# List all Adblock Plus options (excepting domain, which is handled separately), as of version 1.3.9
KNOWNOPTIONS = ("badfilter", "collapse", "doc", "document", "elemhide", "empty", "font",
                "genericblock", "generichide", "image", "important", "inline-script",
                "match-case", "media", "object", "object-subrequest", "other", "ping", "popunder", "popup",
                "script", "stylesheet", "subdocument",  "first-party", "third-party",
                "websocket", "webrtc", "xmlhttprequest")
# List of known key=value parameters (domain is not included)
KNOWNPARAMETERS = ("csp", "queryprune", "rewrite", "redirect", "redirect-rule")

# List the supported revision control system commands
REPODEF = collections.namedtuple("repodef", "name, directory, locationoption, repodirectoryoption, checkchanges, difference, pull, checkupdate, update, merge, commit, push")
GIT = REPODEF(["git"], "./.git/", "--work-tree=", "--git-dir=", ["status", "-s", "--untracked-files=no"], ["diff"], ["pull"], None, None, ["merge"], ["commit", "-am"], ["push"])
HG = REPODEF(["hg"], "./.hg/", "-R", None, ["stat", "-q"], ["diff"], ["pull"], ["update", "--check"], ["update"], ["merge"], ["commit", "-m"], ["push"])
REPOTYPES = (GIT, HG)

def start ():
    """ Print a greeting message and run FOP in the directories
    specified via the command line, or the current working directory if
    no arguments have been passed."""
    greeting = "FOP (Filter Orderer and Preener) version {version}".format(version = VERSION)
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

def main (location):
    """ Find and sort all the files in a given directory, committing
    changes to a repository if one exists."""
    # Check that the directory exists, otherwise return
    if not os.path.isdir(location):
        print("{location} does not exist or is not a folder.".format(location = location))
        return

    # Set the repository type based on hidden directories
    repository = None
    for repotype in REPOTYPES:
        if os.path.isdir(os.path.join(location, repotype.directory)):
            repository = repotype
            break
    # If this is a repository, record the initial changes; if this fails, give up trying to use the repository
    if repository:
        try:
            basecommand = repository.name
            if repository.locationoption.endswith("="):
                basecommand.append("{locationoption}{location}".format(locationoption = repository.locationoption, location = location))
            else:
                basecommand.extend([repository.locationoption, location])
            if repository.repodirectoryoption:
                if repository.repodirectoryoption.endswith("="):
                    basecommand.append("{repodirectoryoption}{location}".format(repodirectoryoption = repository.repodirectoryoption, location = os.path.normpath(os.path.join(location, repository.directory))))
                else:
                    basecommand.extend([repository.repodirectoryoption, location])
            command = basecommand + repository.checkchanges
            originaldifference = True if subprocess.check_output(command) else False
        except(subprocess.CalledProcessError, OSError):
            print("The command \"{command}\" was unable to run; FOP will therefore not attempt to use the repository tools. On Windows, this may be an indication that you do not have sufficient privileges to run FOP - the exact reason why is unknown. Please also ensure that your revision control system is installed correctly and understood by FOP.".format(command = " ".join(command)))
            repository = None

    # Work through the directory and any subdirectories, ignoring hidden directories
    print("\nPrimary location: {folder}".format(folder = os.path.join(os.path.abspath(location), "")))
    for path, directories, files in os.walk(location):
        for direct in directories[:]:
            if direct.startswith(".") or direct in IGNORE:
                directories.remove(direct)
        print("Current directory: {folder}".format(folder = os.path.join(os.path.abspath(path), "")))
        directories.sort()
        for filename in sorted(files):
            address = os.path.join(path, filename)
            extension = os.path.splitext(filename)[1]
            # Sort all text files that are not blacklisted
            if extension == ".txt" and filename not in IGNORE:
                fopsort(address)
            # Delete unnecessary backups and temporary files
            if extension == ".orig" or extension == ".temp":
                try:
                    os.remove(address)
                except(IOError, OSError):
                    # Ignore errors resulting from deleting files, as they likely indicate that the file has already been deleted
                    pass

    # If in a repository, offer to commit any changes
    if repository:
        commit(repository, basecommand, originaldifference)

def fopsort (filename):
    """ Sort the sections of the file and save any modifications."""
    temporaryfile = "{filename}.temp".format(filename = filename)
    CHECKLINES = 10
    section = []
    lineschecked = 1
    filterlines = elementlines = 0

    # Read in the input and output files concurrently to allow filters to be saved as soon as they are finished with
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
                            # do not combine rules containing included domains with rules containing only excluded domains
                            combinedFilters.append(uncombinedFilters[i])
                        else:
                            # either both contain one or more included domains, or both contain only excluded domains
                            domainssubstitute = domains1.group(0).replace(domain1str, newDomains, 1)
                            uncombinedFilters[i+1] = re.sub(DOMAINPATTERN, domainssubstitute, uncombinedFilters[i])
                    else:
                        # non-identical filters shouldn't be combined
                        combinedFilters.append(uncombinedFilters[i])
            return combinedFilters


        # Writes the filter lines to the file
        def writefilters():
            if elementlines > filterlines:
                uncombinedFilters = sorted(set(section), key = lambda rule: re.sub(ELEMENTDOMAINPATTERN, "", rule))
                outputfile.write("{filters}\n".format(filters = "\n".join(combinefilters(uncombinedFilters, ELEMENTDOMAINPATTERN, ","))))
            else:
                uncombinedFilters = sorted(set(section), key = str.lower)
                outputfile.write("{filters}\n".format(filters = "\n".join(combinefilters(uncombinedFilters, FILTERDOMAINPATTERN, "|"))))

        for line in inputfile:
            line = line.strip()
            if re.match(BLANKPATTERN, line):
                continue
            # Include comments verbatim and, if applicable, sort the preceding section of filters and save them in the new version of the file
            if line[0] == "!" or line[:8] == "%include" or line[0] == "[" and line[-1] == "]":
                if section:
                    writefilters()
                    section = []
                    lineschecked = 1
                    filterlines = elementlines = 0
                outputfile.write("{line}\n".format(line = line))
            else:
                # Neaten up filters and, if necessary, check their type for the sorting algorithm
                elementparts = re.match(ELEMENTPATTERN, line)
                if elementparts:
                    domains = elementparts.group(1).lower()
                    if lineschecked <= CHECKLINES:
                        elementlines += 1
                        lineschecked += 1
                    line = elementtidy(domains, elementparts.group(2), elementparts.group(3))
                else:
                    if lineschecked <= CHECKLINES:
                        filterlines += 1
                        lineschecked += 1
                    line = filtertidy(line)
                # Add the filter to the section
                section.append(line)
        # At the end of the file, sort and save any remaining filters
        if section:
            writefilters()

    # Replace the existing file with the new one only if alterations have been made
    if not filecmp.cmp(temporaryfile, filename):
        # Check the operating system and, if it is Windows, delete the old file to avoid an exception (it is not possible to rename files to names already in use on this operating system)
        if os.name == "nt":
            os.remove(filename)
        os.rename(temporaryfile, filename)
        print("Sorted: {filename}".format(filename = os.path.abspath(filename)))
    else:
        os.remove(temporaryfile)

def sortfunc (option):
    # For identical options, the inverse always follows the non-inverse option ($image,~image instead of $~image,image) with exception for popup filter
    if option[0] == "~": return option[1:] + "{"
    if option == "popup": return option + "}"
    # Also let third-party will always be first in the list
    if option.find("third-party") > -1: return "0" + option
    # And let badfilter and key=value parameters will always be last in the list
    if option.find("badfilter") > -1: return "|" + option
    if option.split('=')[0] in KNOWNPARAMETERS: return "}" + option
    return option

def filtertidy (filterin):
    """ Sort the options of blocking filters and make the filter text
    lower case if applicable."""
    optionsplit = re.match(OPTIONPATTERN, filterin)

    if not optionsplit:
        # Remove unnecessary asterisks from filters without any options and return them
        return removeunnecessarywildcards(filterin, False)
    else:
        # If applicable, separate and sort the filter options in addition to the filter text
        optionlist = optionsplit.group(2).lower().split(",")

        domainlist = []
        removeentries = []
        queryprune = ""
        rediwritelist = []
        keepAsterisk = False
        for option in optionlist:
            # Detect and separate domain options
            if option[0:7] == "domain=":
                domainlist.extend(option[7:].split("|"))
                removeentries.append(option)
            elif option[0:11] == "queryprune=":
                queryprune = option[11:]
                removeentries.append(option)
            elif re.match(REDIWRITEOPTIONPATTERN, option):
                keepAsterisk = True
                rediwritelist.append(option)
            elif option == "popunder":
                keepAsterisk = True
            elif option.strip("~") not in KNOWNOPTIONS and option.split('=')[0] not in KNOWNPARAMETERS:
                print("Warning: The option \"{option}\" used on the filter \"{problemfilter}\" is not recognised by FOP".format(option = option, problemfilter = filterin))
        # Sort all options other than domain alphabetically with a few exceptions
        optionlist = sorted(set(filter(lambda option: (option not in removeentries) and (option not in rediwritelist), optionlist)), key = sortfunc)
        # Replace underscore typo with hyphen-minus in options like third_party
        optionlist = list(map(lambda option: option.replace("_", "-"), optionlist))
        # Append queryprune back at the end (both to keep it at the end and skip underscore typo fix)
        if queryprune:
            optionlist.append("queryprune={queryprune}".format(queryprune = queryprune))
        # Append redirect rule back without underscore typo fix
        if rediwritelist:
            optionlist.extend(rediwritelist)
        # If applicable, sort domain restrictions and append them to the list of options
        if domainlist:
            optionlist.append("domain={domainlist}".format(domainlist = "|".join(sorted(set(domainlist), key = lambda domain: domain.strip("~")))))

        # according to uBO documentation redirect options must start either with * or ||
        # so, it is not unnecessary wildcard in such case
        filtertext = removeunnecessarywildcards(optionsplit.group(1), keepAsterisk)
        if keepAsterisk and filtertext[0] != '*' and filtertext[:2] != '||':
            print("Warning: Incorrect filter \"{filterin}\". Such filters must start with either '*' or '||'.".format(filterin = filterin))
        # Return the full filter
        return "{filtertext}${options}".format(filtertext = filtertext, options = ",".join(optionlist))

def elementtidy (domains, separator, selector):
    """ Sort the domains of element hiding rules, remove unnecessary
    tags and make the relevant sections of the rule lower case."""
    # Order domain names alphabetically, ignoring exceptions
    if "," in domains:
        domains = ",".join(sorted(set(domains.split(",")), key = lambda domain: domain.strip("~")))
    # Skip non-selectors (uBO's JS injections and other)
    if re.match(NONSELECTOR, selector) != None:
        return "{domain}{separator}{selector}".format(domain = domains, separator = separator, selector = selector)
    # Mark the beginning and end of the selector with "@"
    selectorandtail = re.match(SELECTORANDTAILPATTERN, selector) #selector.split(':style(')
    splitterpart = ""
    tailpart = ""
    if selectorandtail.group(2) != None:
        splitterpart = selectorandtail.group(3)
        tailpart = selectorandtail.group(4)
    selector = "@{selector}@".format(selector = selectorandtail.group(1))
    each = re.finditer
    # Make sure we don't match items in strings (e.g., don't touch Width in ##[style="height:1px; Width: 123px;"])
    selectorwithoutstrings = selector
    selectoronlystrings = ""
    while True:
        stringmatch = re.match(ATTRIBUTEVALUEPATTERN, selectorwithoutstrings)
        if stringmatch == None: break
        selectorwithoutstrings = selectorwithoutstrings.replace("{before}{stringpart}".format(before = stringmatch.group(1), stringpart = stringmatch.group(2)), "{before}".format(before = stringmatch.group(1)), 1)
        selectoronlystrings = "{old}{new}".format(old = selectoronlystrings, new = stringmatch.group(2))
    # Clean up tree selectors
    for tree in each(TREESELECTOR, selector):
        if tree.group(0) in selectoronlystrings or not tree.group(0) in selectorwithoutstrings: continue
        # added check for case when tree selector were used in :-abp-has() and similar constructions at first position
        # basically for cases like PARENT:-abp-has(> CHILD)
        replaceby = "{sp}{g2} ".format(sp = ("" if tree.group(1) == "(" else " "), g2 = tree.group(2))
        if replaceby == "   ": replaceby = " "
        selector = selector.replace(tree.group(0), "{g1}{replaceby}{g3}".format(g1 = tree.group(1), replaceby = replaceby, g3 = tree.group(3)), 1)
    # Remove unnecessary tags
    for untag in each(REMOVE_AST_PATTERN, selector):
        untagname = untag.group(4)
        if untagname in selectoronlystrings or not untagname in selectorwithoutstrings: continue
        bc = untag.group(2)
        if bc == None:
            bc = untag.group(3)
        ac = untag.group(5)
        selector = selector.replace("{before}{untag}{after}".format(before = bc, untag = untagname, after = ac), "{before}{after}".format(before = bc, after = ac), 1)
    # Make the remaining tags lower case wherever possible
    for tag in each(SELECTORPATTERN, selector):
        tagname = tag.group(1)
        if tagname in selectoronlystrings or not tagname in selectorwithoutstrings: continue
        if re.search(UNICODESELECTOR, selectorwithoutstrings) != None: break
        ac = tag.group(3)
        if ac == None:
            ac = tag.group(4)
        selector = selector.replace("{tag}{after}".format(tag = tagname, after = ac), "{tag}{after}".format(tag = tagname.lower(), after = ac), 1)
    # Make pseudo classes lower case where possible
    for pseudo in each(PSEUDOPATTERN, selector):
        pseudoclass = pseudo.group(1)
        if pseudoclass in selectoronlystrings or not pseudoclass in selectorwithoutstrings: continue
        ac = pseudo.group(2)
        selector = selector.replace("{pclass}{after}".format(pclass = pseudoclass, after = ac), "{pclass}{after}".format(pclass = pseudoclass.lower(), after = ac), 1)
    # Remove unnecessary 'px' in '0px' and space in "! important"
    if splitterpart == ":style" and tailpart != None:
        for un0px in each(REMOVE_0PX_PATTERN, tailpart):
            bc = un0px.group(2)
            ac = un0px.group(4)
            tailpart = tailpart.replace("{before}{remove}{after}".format(before = bc, remove = un0px.group(3), after = ac), "{before}{after}".format(before = bc, after = ac), 1)
        for bsi in each(BANGSPACEIMPORTANT, tailpart):
            bc = bsi.group(1)
            space = "" if bc == " " else " "
            ac = bsi.group(3)
            tailpart = tailpart.replace("{before}{bang}{after}".format(before = bc, bang = bsi.group(2), after = ac), "{before}{space}!{after}".format(before = bc, space = space, after = ac), 1)
    # Remove the markers from the beginning and end of the selector and return the complete rule
    return "{domain}{separator}{selector}{splitter}{tail}".format(domain = domains, separator = separator, selector = selector[1:-1], splitter = splitterpart, tail = tailpart)

def commit (repository, basecommand, userchanges):
    """ Commit changes to a repository using the commands provided."""
    difference = subprocess.check_output(basecommand + repository.difference)
    if not difference:
        print("\nNo changes have been recorded by the repository.")
        return
    print("\nThe following changes have been recorded by the repository:")
    try:
        print(difference.decode("utf-8"))
    except UnicodeEncodeError:
        print("\nERROR: DIFF CONTAINED UNKNOWN CHARACTER(S). Showing unformatted diff instead:\n")
        print(difference)
    try:
        # Persistently request a suitable comment
        while True:
            comment = input("Please enter a valid commit comment or quit:\n")
            if checkcomment(comment, userchanges):
                break
    # Allow users to abort the commit process if they do not approve of the changes
    except (KeyboardInterrupt, SystemExit):
        print("\nCommit aborted.")
        return

    print("Comment \"{comment}\" accepted.".format(comment = comment))
    try:
        print("\nConnecting to server. Please enter your password if required.")
        # Update the server repository as required by the revision control system
        for command in repository[6:]:
            if command == None:
                continue
            if command == repository.commit:
                command += [comment]
            command = basecommand + command
            subprocess.Popen(command).communicate()
            print()
    except(subprocess.CalledProcessError):
        print("Unexpected error with the command \"{command}\".".format(command = command))
        raise subprocess.CalledProcessError("Aborting FOP.", command)
    except(OSError):
        print("Unexpected error with the command \"{command}\".".format(command = command))
        raise OSError("Aborting FOP.")
    print("Completed commit process successfully.")

def isglobalelement (domains):
    """ Check whether all domains are negations."""
    for domain in domains.split(","):
        if domain and not domain.startswith("~"):
            return False
    return True

def removeunnecessarywildcards (filtertext, keepAsterisk):
    """ Where possible, remove unnecessary wildcards from the beginnings
    and ends of blocking filters."""
    allowlist = False
    hadStar = False
    if filtertext[0:2] == "@@":
        allowlist = True
        filtertext = filtertext[2:]
    while len(filtertext) > 1 and filtertext[0] == "*" and not filtertext[1] == "|" and not filtertext[1] == "!":
        filtertext = filtertext[1:]
        hadStar = True
    while len(filtertext) > 1 and filtertext[-1] == "*" and not filtertext[-2] == "|" and not filtertext[-2] == " ":
        filtertext = filtertext[:-1]
        hadStar = True
    if hadStar and filtertext[0] == "/" and filtertext[-1] == "/":
        filtertext = "{filtertext}*".format(filtertext = filtertext)
    if hadStar and keepAsterisk:
        filtertext = "*{filtertext}".format(filtertext = filtertext)
    if not keepAsterisk and filtertext == "*":
        filtertext = ""
    if allowlist:
        filtertext = "@@{filtertext}".format(filtertext = filtertext)
    return filtertext

def checkcomment(comment, changed):
    """ Check the commit comment and return True if the comment is
    acceptable and False if it is not."""
    sections = re.match(COMMITPATTERN, comment)
    if sections == None:
        print("The comment \"{comment}\" is not in the recognised format.".format(comment = comment))
    else:
        indicator = sections.group(1)
        if indicator == "M":
            # Allow modification comments to have practically any format
            return True
        elif indicator == "A" or indicator == "P":
            if not changed:
                print("You have indicated that you have added or removed a rule, but no changes were initially noted by the repository.")
            else:
                address = sections.group(4)
                if not validurl(address):
                    print("Unrecognised address \"{address}\".".format(address = address))
                else:
                    # The user has changed the subscription and has written a suitable comment message with a valid address
                    return True
    print()
    return False

def validurl (url):
    """ Check that an address has a scheme (e.g. http), a domain name
    (e.g. example.com) and a path (e.g. /), or relates to the internal
    about system."""
    addresspart = urlparse(url)
    if addresspart.scheme and addresspart.netloc and addresspart.path:
        return True
    elif addresspart.scheme == "about":
        return True
    else:
        return False

if __name__ == '__main__':
    start()
