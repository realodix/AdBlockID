#!/bin/bash

flrender -i abid=. vendor/ffromvendor/filter.adbl ffromvendor.txt

# cleanup
sed '/^!/d' -i ffromvendor.txt
sed '/^#/d' -i ffromvendor.txt
sed '/Adblock/d' -i ffromvendor.txt

python vendor/fop/FOP.py

flrender -i abid=. adblockid.adbl output/adblockid.txt

vendor/readme/readme.sh

rm ffromvendor.txt
