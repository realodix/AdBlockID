import re
import sort, var


""" Sort the domains of element hiding rules, remove unnecessary tags and make the
    relevant sections of the rule lower case."""
def elementtidy (domains, separator, selector):
    # Order domain names alphabetically, ignoring exceptions
    if "," in domains:
        domains = ",".join(sorted(set(domains.split(",")), key = lambda domain: domain.strip("~")))

    # Skip non-selectors (uBO's JS injections and other)
    if re.match(var.NONSELECTOR, selector) != None:
        return "{domain}{separator}{selector}".format(domain = domains, separator = separator, selector = selector)

    # Mark the beginning and end of the selector with "@"
    selectorandtail = re.match(var.SELECTORANDTAILPATTERN, selector) #selector.split(':style(')
    splitterpart = ""
    tailpart = ""

    if selectorandtail.group(2) != None:
        splitterpart = selectorandtail.group(3)
        tailpart = selectorandtail.group(4)

    selector = "@{selector}@".format(selector = selectorandtail.group(1))
    each = re.finditer
    # Make sure we don't match items in strings (e.g., don't touch Width in
    # ##[style="height:1px; Width: 123px;"])
    selectorwithoutstrings = selector
    selectoronlystrings = ""

    while True:
        stringmatch = re.match(var.ATTRIBUTEVALUEPATTERN, selectorwithoutstrings)
        if stringmatch == None: break
        selectorwithoutstrings = selectorwithoutstrings.replace("{before}{stringpart}".format(before = stringmatch.group(1), stringpart = stringmatch.group(2)), "{before}".format(before = stringmatch.group(1)), 1)
        selectoronlystrings = "{old}{new}".format(old = selectoronlystrings, new = stringmatch.group(2))

    # Clean up tree selectors
    for tree in each(var.TREESELECTOR, selector):
        if tree.group(0) in selectoronlystrings or not tree.group(0) in selectorwithoutstrings: continue

        # Added check for case when tree selector were used in :-abp-has() and similar
        # constructions at first position. Basically for cases like
        # PARENT:-abp-has(> CHILD)
        replaceby = "{sp}{g2} ".format(sp = ("" if tree.group(1) == "(" else " "), g2 = tree.group(2))

        if replaceby == "   ": replaceby = " "

        selector = selector.replace(tree.group(0), "{g1}{replaceby}{g3}".format(g1 = tree.group(1), replaceby = replaceby, g3 = tree.group(3)), 1)

    # Remove unnecessary tags
    for untag in each(var.REMOVE_AST_PATTERN, selector):
        untagname = untag.group(4)

        if untagname in selectoronlystrings or not untagname in selectorwithoutstrings: continue
        bc = untag.group(2)

        if bc == None:
            bc = untag.group(3)

        ac = untag.group(5)
        selector = selector.replace("{before}{untag}{after}".format(before = bc, untag = untagname, after = ac), "{before}{after}".format(before = bc, after = ac), 1)

    # Make the remaining tags lower case wherever possible
    for tag in each(var.SELECTORPATTERN, selector):
        tagname = tag.group(1)
        if tagname in selectoronlystrings or not tagname in selectorwithoutstrings: continue
        if re.search(var.UNICODESELECTOR, selectorwithoutstrings) != None: break

        ac = tag.group(3)

        if ac == None:
            ac = tag.group(4)

        selector = selector.replace("{tag}{after}".format(tag = tagname, after = ac), "{tag}{after}".format(tag = tagname.lower(), after = ac), 1)

    # Make pseudo classes lower case where possible
    for pseudo in each(var.PSEUDOPATTERN, selector):
        pseudoclass = pseudo.group(1)

        if pseudoclass in selectoronlystrings or not pseudoclass in selectorwithoutstrings: continue

        ac = pseudo.group(2)
        selector = selector.replace("{pclass}{after}".format(pclass = pseudoclass, after = ac), "{pclass}{after}".format(pclass = pseudoclass.lower(), after = ac), 1)

    # Remove unnecessary 'px' in '0px' and space in "! important"
    if splitterpart == ":style" and tailpart != None:
        for un0px in each(var.REMOVE_0PX_PATTERN, tailpart):
            bc = un0px.group(2)
            ac = un0px.group(4)
            tailpart = tailpart.replace("{before}{remove}{after}".format(before = bc, remove = un0px.group(3), after = ac), "{before}{after}".format(before = bc, after = ac), 1)
        for bsi in each(var.BANGSPACEIMPORTANT, tailpart):
            bc = bsi.group(1)
            space = "" if bc == " " else " "
            ac = bsi.group(3)
            tailpart = tailpart.replace("{before}{bang}{after}".format(before = bc, bang = bsi.group(2), after = ac), "{before}{space}!{after}".format(before = bc, space = space, after = ac), 1)

    # Remove the markers from the beginning and end of the selector and return the
    # complete rule
    return "{domain}{separator}{selector}{splitter}{tail}".format(domain = domains, separator = separator, selector = selector[1:-1], splitter = splitterpart, tail = tailpart)



""" Sort the options of blocking filters and make the filter text lower case if
    applicable."""
def filtertidy (filterin):
    optionsplit = re.match(var.OPTIONPATTERN, filterin)

    if not optionsplit:
        # Remove unnecessary asterisks from filters without any options and return them
        return removeunnecessarywildcards(filterin, False)
    else:
        # If applicable, separate and sort the filter options in addition to the filter
        # text
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
            elif re.match(var.REDIWRITEOPTIONPATTERN, option):
                # keepAsterisk = True
                rediwritelist.append(option)
            elif option == "popunder":
                keepAsterisk = True
            elif option.strip("~") not in var.KNOWNOPTIONS and option.split('=')[0] not in var.KNOWNPARAMETERS:
                print("Warning: The option \"{option}\" used on the filter \"{problemfilter}\" is not recognised by FOP".format(option = option, problemfilter = filterin))

        # Sort all options other than domain alphabetically with a few exceptions
        optionlist = sorted(set(filter(lambda option: (option not in removeentries) and (option not in rediwritelist), optionlist)), key = sort.sortfunc)
        # Replace underscore typo with hyphen-minus in options like third_party
        optionlist = list(map(lambda option: option.replace("_", "-"), optionlist))

        # Append queryprune back at the end (both to keep it at the end and skip
        # underscore typo fix)
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



""" Where possible, remove unnecessary wildcards from the beginnings and ends of blocking
    filters."""
def removeunnecessarywildcards (filtertext, keepAsterisk):
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
