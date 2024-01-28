#!/bin/bash

FOP="python tools/fop/fop.py -d src tests"
ADBLOCKID="flcombine -i abid=. template/adblockid.template.txt dist/adblockid.adfl.txt"
ADBLOCKID_PLUS="flcombine -i abid=. template/adblockid_plus.template.txt dist/adblockid_plus.adfl.txt"

if [ "$1" == "fop" ]; then
    eval $FOP
fi

if [ "$1" == "abid" ]; then
    eval $FOP
    eval $ADBLOCKID
fi

if [ "$1" == "abidplus" ]; then
    eval $FOP
    eval $ADBLOCKID_PLUS
fi

if [ $# -eq 0 ]; then
    eval $FOP
    eval $ADBLOCKID
    eval $ADBLOCKID_PLUS
fi

# read -t 7 -p "Press any key to continue... " -n 1
