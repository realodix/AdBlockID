#!/bin/bash

# cleanup
python tools/fop/FOP.py

# Gabungkan semua filter, termasuk thirdparties filter
flrender -i abid=. src/template/adblockid.adbl output/adblockid.txt
flrender -i abid=. src/template/adblockid.adbl output/adblockid-plus.txt

# Update versi dan tanggal pada file readme
tools/readme/readme.sh
