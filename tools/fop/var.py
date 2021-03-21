import collections, re

VERSION = "1.1"
SECTIONS_EXT = "adbl"

# Compile regular expressions to match important filter parts (derived from Wladimir
# Palant's Adblock Plus source code)
ELEMENTDOMAINPATTERN = re.compile(r"^([^\/\*\|\@\"\!]*?)#[@$?]?#")
FILTERDOMAINPATTERN = re.compile(r"(?:\$|\,)domain\=([^\,\s]+)$")
ELEMENTPATTERN = re.compile(r"^([^\/\*\|\@\"\!]*?)(#[@$?]?#)([^{}]+)$")
OPTIONPATTERN = re.compile(r"^(.*)\$(~?[\w\-]+(?:=[^,\s]+)?(?:,~?[\w\-]+(?:=[^,\s]+)?)*)$")
REDIWRITEOPTIONPATTERN = re.compile(r"^(redirect(-rule)?|rewrite)=")

# Compile regular expressions that match element tags and pseudo classes and strings and
# tree selectors; "@" indicates either the beginning or the end of a selector
SELECTORPATTERN = re.compile(r"(?<=[\s\[@])([a-zA-Z]*[A-Z][a-zA-Z0-9]*)((?=([\[\]\^\*\$=:@#\.]))|(?=(\s(?:[+>~]|\*|[a-zA-Z][a-zA-Z0-9]*[\[:@\s#\.]|[#\.][a-zA-Z][a-zA-Z0-9]*))))")
PSEUDOPATTERN = re.compile(r"(\:[a-zA-Z\-]*[A-Z][a-zA-Z\-]*)(?=([\(\:\@\s]))")
# (?!:-) - skip Adblock Plus' :-abp-... pseudoclasses, (?!:style\() - skip uBlock Origin's
# :style() pseudoclass
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

# List the files that should not be sorted, either because they have a special sorting
# system or because they are not filter files
IGNORE = ("adblockid.txt", "docs", "tools", "template")

# List all Adblock Plus options (excepting domain, which is handled separately), as of
# version 1.3.9
KNOWNOPTIONS = (
    # ABP
    # https://help.eyeo.com/en/adblockplus/how-to-write-filters#options
    "document", "elemhide", "font", "genericblock", "generichide", "image", "match-case", "media", "object", "other", "ping", "popup", "script", "stylesheet", "subdocument", "third-party", "webrtc", "websocket", "xmlhttprequest",

    # uBlock Origin
    # https://github.com/gorhill/uBlock/wiki/Static-filter-syntax
    "1p", "first-party", "3p", "all", "badfilter", "cname", "csp", "css", "denyallow", "doc", "ehide", "frame", "ghide", "important", "inline-font", "inline-script", "mp4", "object-subrequest", "popunder", "shide", "specifichide", "strict1p", "strict3p", "xhr",

    # AdGuard
    # https://kb.adguard.com/en/general/how-to-create-your-own-ad-filters
    "content", "extension", "jsinject", "network", "stealth", "urlblock"
)

# List of known key=value parameters (domain is not included)
KNOWNPARAMETERS = (
    # ABP
    "rewrite",

    # uBO
    "csp", "redirect", "redirect-rule", "removeparam",

    # AdGuard
    "app", "cookie", "replace"
)
