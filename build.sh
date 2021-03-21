#!/bin/bash

# cleanup
python tools/fop/fop.py

# Gabungkan semua filter, termasuk thirdparties filter
flrender -i abid=. src/template/adblockid.adbl output/adblockid.txt
