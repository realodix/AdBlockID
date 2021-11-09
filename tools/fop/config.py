#!/usr/bin/env python3
""" Filter Orderer and Preener

Adjusted for AdBlockID
Based on FOP (RU AdList) v3.921

Copyright (C) 2011 Michael
GNU General Public License
"""

import re

VERSION = "1.7"
SECTIONS_EXT = [".txt", ".adbl"]
# List the files that should not be sorted, either because they have a special sorting
# system or because they are not filter files
IGNORE = ("adblockid.txt", "docs", "tools", "template", "international.adbl", "python-abp"
    "python-abp", "python-abp_AdBlockID", "VICHS_AdBlockID")

# Regex to match important filter parts
RE_ELEMENTDOMAIN = re.compile(r"^([^\/\*\|\@\"\!]*?)#[@$?]?#")
RE_FILTERDOMAIN = re.compile(r"(?:\$|\,)domain\=([^\,\s]+)$")
RE_ELEMENT = re.compile(r"^([^\/\*\|\@\"\!]*?)(#[@$?]?#)([^{}]+)$")
RE_OPTION= re.compile(r"^(.*)\$(~?[\w\-]+(?:=[^,\s]+)?(?:,~?[\w\-]+(?:=[^,\s]+)?)*)$")
RE_REDIWRITEOPTION = re.compile(r"^(redirect(-rule)?|rewrite)=")

# Regex to match element tags, pseudo classes, strings and tree selectors; "@" indicates
# either the beginning or the end of a selector
RE_SELECTOR = re.compile(r"""
  (?<=[\s\[@])
  ([a-zA-Z]*[A-Z][a-zA-Z0-9]*)
  (
    (?=([\[\]\^\*\$=:@#\.]))
    | (?=(\s(
      ?:[+>~]
      | \*|[a-zA-Z][a-zA-Z0-9]*[\[:@\s#\.]
      | [#\.][a-zA-Z][a-zA-Z0-9]*
    )))
  )
""")
RE_PSEUDO = re.compile(r"(\:[a-zA-Z\-]*[A-Z][a-zA-Z\-]*)(?=([\(\:\@\s]))")
# (?!:-) - skip ABP `:-abp-...` pseudoclasses
# (?!:style\() - skip uBO `:style()` pseudoclass
RE_REMOVE_AST = re.compile(r"""
  (
    (?<=([>+~,]\s))
    | (?<=(@|\s|,))
  )
  (\*)
  (?=([#\.\[\:]))
  (?!:-)
  (?!:style\()
""")
RE_SELECTORSTYLEPART = re.compile(r":style\(.+\)$")
RE_REMOVE_0PX = re.compile(r"((?<=([\:\s]0))(px)(?=([\s\!])))")
RE_BANGSPACEIMPORTANT = re.compile(r"(.)(\!\s)(important)")
RE_ATTRIBUTEVALUE = re.compile(r"^([^\'\"\\]|\\.)*(\"(?:[^\"\\]|\\.)*\"|\'(?:[^\'\\]|\\.)*\')")
RE_TREESELECTOR = re.compile(r"(\\.|[^\+\>\~\\\ \t])\s*([\+\>\~\ \t])\s*(\D)")
RE_UNICODESELECTOR = re.compile(r"\\[0-9a-fA-F]{1,6}\s[a-zA-Z]*[A-Z]")
RE_NONSELECTOR = re.compile(r"^(\+js\(|script:inject\()")
RE_SELECTORANDTAIL = re.compile(r"^(.*?)((:-abp-contains|:style|:matches-css)(.*))?$")

# Regex that describes a completely blank line
RE_BLANKLINE = re.compile(r"^\s*$")

# List all options (excepting domain and `KNOWNPARAMETERS`, which is handled separately)
KNOWNOPTIONS = (
    # ABP
    # https://help.eyeo.com/en/adblockplus/how-to-write-filters#options
    "document", "elemhide", "font", "genericblock", "generichide", "image", "match-case",
    "media", "object", "other", "ping", "popup", "script", "stylesheet", "subdocument",
    "third-party", "webrtc", "websocket", "xmlhttprequest",

    # uBlock Origin
    # https://github.com/gorhill/uBlock/wiki/Static-filter-syntax
    "1p", "first-party", "strict1p", "3p", "strict3p", "all", "badfilter", "cname", "csp",
    "css", "doc", "ehide", "frame", "ghide", "important", "inline-font", "inline-script",
    "mp4", "object-subrequest", "popunder", "shide", "specifichide", "xhr"
)

# List of known key=value parameters (domain is not included)
KNOWNPARAMETERS = (
    # ABP
    "rewrite",

    # uBO
    "csp", "denyallow", "redirect", "redirect-rule", "removeparam"
)
