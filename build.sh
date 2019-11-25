#!/bin/bash

# Render thirdparties filter dan buat file thirdparties-filter.txt
flrender -i abid=. src/template/thirdparties.adbl thirdparties-filter.txt

# cleanup
sed '/^!/d' -i thirdparties-filter.txt
sed '/^#/d' -i thirdparties-filter.txt
sed '/Adblock/d' -i thirdparties-filter.txt
python tools/fop/FOP.py

# Gabungkan semua filter, termasuk thirdparties filter
flrender -i abid=. src/template/adblockid.adbl output/adblockid.txt

# Update versi dan tanggal pada file readme
tools/readme/readme.sh

# Hapus thirdparties-filter.txt, karena sudah tidak digunakan lagi
rm thirdparties-filter.txt

# Khusus untuk AdGuard
# https://github.com/AdguardTeam/FiltersRegistry/issues/259
# https://github.com/AdguardTeam/FiltersCompiler/issues/41
cp ./src/addons/adult-hide.adbl ./src/addons/adult-hide-adguard.adbl
sed -i 's/" i]/"]/g' src/addons/adult-hide-adguard.adbl
