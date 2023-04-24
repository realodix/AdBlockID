#!/bin/bash

FOP="python tools/fop/fop.py -d src dist -i adblockid.adfl.txt adblockid_plus.adfl.txt"

if [ "$1" == "fop" ]; then
    eval $FOP
fi

if [ "$1" == "abid" ]; then
    eval $FOP
    eval "flcombine -i abid=. template/adblockid.template.txt dist/adblockid.adfl.txt"
fi

if [ "$1" == "abidplus" ]; then
    eval $FOP
    eval "flcombine -i abid=. src/packages/adblockid_plus.template.txt dist/adblockid_plus.adfl.txt"
fi

read -t 7 -p "Press any key to continue... " -n 1
