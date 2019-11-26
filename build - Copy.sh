#!/bin/bash

# Khusus untuk AdGuard
# https://github.com/AdguardTeam/FiltersRegistry/issues/259
# https://github.com/AdguardTeam/FiltersCompiler/issues/41
cp ./src/addons/adult-hide.adbl ./src/addons/adult-hide-adguard.adbl
sed -i 's/" i]/"]/g' src/addons/adult-hide-adguard.adbl
sed -i '/[1-9]\./d' src/addons/adult-hide-adguard.adbl
sed -i '/alt\*/d' src/addons/adult-hide-adguard.adbl
sed -i '/title/d' src/addons/adult-hide-adguard.adbl
