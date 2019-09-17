#!/bin/sh

flrender -i abid=. addons/vendor.adbl content.txt

# cleanup
sed '/^!/d' -i content.txt
sed '/^#/d' -i content.txt
sed '/Adblock/d' -i content.txt

python FOP.py

flrender -i abid=. adblockid.adbl output/adblockid.txt

rm content.txt
