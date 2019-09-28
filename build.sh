#!/bin/bash

flrender -i abid=. src/template/thirdparties.adbl thirdparties-filter.txt

# cleanup
sed '/^!/d' -i thirdparties-filter.txt
sed '/^#/d' -i thirdparties-filter.txt
sed '/Adblock/d' -i thirdparties-filter.txt

python vendor/fop/FOP.py

flrender -i abid=. src/template/adblockid.adbl output/adblockid.txt

vendor/readme/readme.sh

rm thirdparties-filter.txt
