#!/bin/bash

# cleanup
python tools/fop/fop.py

# Gabungkan semua filter, termasuk thirdparties filter
flcombine -i abid=. template/adblockid.template.txt output/adblockid.txt
flcombine -i abid=. src/packages/adblockid_plus.template.txt output/adblockid_plus.txt
