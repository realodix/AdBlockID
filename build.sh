#!/bin/bash

FOP="python tools/fop/fop.py -d src output -i adblockid.txt adblockid_plus.txt personal.txt"

if [ "$1" == "fop" ]; then
    eval $FOP
fi

if [ "$1" == "abid" ]; then
    eval $FOP
    eval "flcombine -i abid=. template/adblockid.template.txt output/adblockid.txt"
fi

if [ "$1" == "abidplus" ]; then
    eval $FOP
    eval "flcombine -i abid=. src/packages/adblockid_plus.template.txt output/adblockid_plus.txt"
fi

read -t 7 -p "Press any key to continue... " -n 1
