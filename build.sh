#!/bin/bash

flrender -i abid=. addons/vendor.adbl content.txt

# cleanup
sed '/^!/d' -i content.txt
sed '/^#/d' -i content.txt
sed '/Adblock/d' -i content.txt

python vendor/fop/FOP.py

flrender -i abid=. adblockid.adbl output/adblockid.txt

vendor/readme/readme.sh

rm content.txt
