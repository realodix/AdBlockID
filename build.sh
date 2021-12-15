#!/bin/bash

# cleanup
python tools/fop/fop.py

# Gabungkan semua filter, termasuk thirdparties filter
flcombine -i abid=. template/adblockid.template.txt output/adblockid.txt
