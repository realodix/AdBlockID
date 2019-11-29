#!/bin/bash

readonly aha="src/addons/adult-hide-adguard.adbl"

# Copy semua filter pada adult-hide.adbl ke dalam adult-hide-adguard.adbl
cp ./src/addons/adult-hide.adbl ./src/addons/adult-hide-adguard.adbl

# Konversi filter
sed -i 's/" i]/"]/g' $aha

# Lakukan pembersihan filter yang tidak perlu
sed -i '/"[0-9]\{1,3\}\./d' $aha
sed -i '/alt\*/d' $aha
sed -i '/title/d' $aha

# Tulis waning pada file adult-hide-adguard.adbl
sed -i '2s/^/! Jangan melakukan perubahan di sini, karena karena file ini (adult-hide-adguard.adbl)\n/' $aha
sed -i '3s/^/! dibuat secara otomatis. File ini digunakan sebagai solusi untuk mengatasi rule pada\n/' $aha
sed -i '4s/^/! fileadult-hide.adbl yang tidak kompatibel dengan AdGuard FiltersCompiler.\n/' $aha
sed -i '5s/^/!\n/' $aha
sed -i '6s/^/! Bug yang terdapat pada AdGuard FiltersCompiler menyebabkan beberapa filter pada AdBlockID\n/' $aha
sed -i '7s/^/! dianggap invalid, sehingga AdBlockID di AdGuard kehilangan kemampuan untuk menghilangkan\n/' $aha
sed -i '8s/^/! iklan berkonten dewasa.\n/' $aha
sed -i '9s/^/!\n/' $aha
sed -i '10s/^/! Info lebih lanjut:\n/' $aha
sed -i '11s/^/! - https:\/\/github.com\/AdguardTeam\/FiltersRegistry\/issues\/259\n/' $aha
sed -i '12s/^/! - https:\/\/github.com\/AdguardTeam\/FiltersCompiler\/issues\/41\n/' $aha

# Gunakan Pre-parsing directives untuk mencegah uBlock Origin dan turunannya
# membaca rule pada adult-hide-adguard.adbl
sed -i '1s/^/!#if false\n/' $aha
sed -i '$s/$/\n!#endif/' $aha

# Format ulang penulisan uBlock Pre-parsing directives yang jadi terlihat typo
# setelah filter dirender oleh python-abp
sed -i 's/! #if false/!#if false/g' output/adblockid.txt
sed -i 's/! #endif/!#endif/g' output/adblockid.txt
