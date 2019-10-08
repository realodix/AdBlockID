#!/bin/bash

# Render thirdparties filter
flrender -i abid=. src/template/thirdparties.adbl thirdparties-filter.txt

# cleanup
sed '/^!/d' -i thirdparties-filter.txt
sed '/^#/d' -i thirdparties-filter.txt
sed '/Adblock/d' -i thirdparties-filter.txt
python tools/fop/FOP.py

flrender -i abid=. src/template/adblockid.adbl output/adblockid.txt

tools/readme/readme.sh

rm thirdparties-filter.txt
