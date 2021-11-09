#!/bin/bash

# cleanup
python tools/fop/fop.py

# Gabungkan semua filter, termasuk thirdparties filter
flcombine -i abid=. template/adblockid.adbl output/adblockid.txt
