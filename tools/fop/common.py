#!/usr/bin/env python3

#
# IGNORE
# -----------------------------------------------------------------------------
# List the files that should not be sorted, either because they have a special
# sorting system or because they are not filter files
# -----------------------------------------------------------------------------

IGNORE = ("adblockid.txt", "docs", "tools", "template")


#
# KNOWNOPTIONS
# -----------------------------------------------------------------------------
# List all Adblock Plus, uBlock Origin and AdGuard options (excepting domain,
# which is handled separately), as of version 1.3.9
# -----------------------------------------------------------------------------

KNOWNOPTIONS = [
    "document", "elemhide", "font", "genericblock", "generichide", "image", "match-case", "media", "object", "other", "ping", "popup", "script", "stylesheet", "subdocument", "third-party", "webrtc", "websocket", "xmlhttprequest",
    "rewrite=abp-resource:blank-css", "rewrite=abp-resource:blank-js", "rewrite=abp-resource:blank-html", "rewrite=abp-resource:blank-mp3", "rewrite=abp-resource:blank-text", "rewrite=abp-resource:1x1-transparent-gif", "rewrite=abp-resource:2x2-transparent-png", "rewrite=abp-resource:3x2-transparent-png", "rewrite=abp-resource:32x32-transparent-png",

    # uBlock Origin
    # https://github.com/gorhill/uBlock/blob/master/src/js/redirect-engine.js
    # https://github.com/gorhill/uBlock/tree/master/src/web_accessible_resources
    "1p", "first-party", "3p", "all", "badfilter", "cname", "csp", "css", "denyallow", "ehide", "empty", "frame", "ghide", "important", "inline-font", "inline-script", "mp4", "object-subrequest", "popunder", "shide", "specifichide", "xhr",
    "redirect=1x1.gif", "redirect-rule=1x1.gif",
    "redirect=2x2.png","redirect-rule=2x2.png",
    "redirect=3x2.png","redirect-rule=3x2.png",
    "redirect=32x32.png", "redirect-rule=32x32.png",
    "redirect=noop.html", "redirect-rule=noop.html",
    "redirect=noop.js", "redirect-rule=noop.js",
    "redirect=noop.txt", "redirect-rule=noop.txt",
    "redirect=noop-0.1s.mp3", "redirect-rule=noop-0.1s.mp3",
    "redirect=noop-1s.mp4","redirect-rule=noop-1s.mp4",
    "redirect=click2load.html", "redirect-rule=click2load.html",
    "redirect=google-analytics_ga.js", "redirect-rule=google-analytics_ga.js",
    "redirect=google-analytics_analytics.js", "redirect-rule=google-analytics_analytics.js",
    "redirect=google-analytics_inpage_linkid.js", "redirect-rule=google-analytics_inpage_linkid.js",
    "redirect=google-analytics_cx_api.js", "redirect-rule=google-analytics_cx_api.js",
    "redirect=googletagservices_gpt.js", "redirect-rule=googletagservices_gpt.js",
    "redirect=googletagmanager_gtm.js", "redirect-rule=googletagmanager_gtm.js",
    "redirect=googlesyndication_adsbygoogle.js", "redirect-rule=googlesyndication_adsbygoogle.js",
    "redirect=fuckadblock.js-3.2.0", "redirect-rule=fuckadblock.js-3.2.0",

    # AdGuard
    "app", "content", "cookie", "extension", "jsinject", "network", "replace", "stealth", "urlblock"
]
