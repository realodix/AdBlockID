#!/bin/bash

readonly aha="src/addons/adult-hide-adguard.adbl"

cp ./src/addons/adult-hide.adbl ./src/addons/adult-hide-adguard.adbl

sed -i 's/" i]/"]/g' $aha
sed -i '/"[0-9]\{1,3\}\./d' $aha
sed -i '/alt\*/d' $aha
sed -i '/title/d' $aha

sed -i '2s/^/! Jangan melakukan perubahan pada file ini (adult-hide-adguard.adbl), karena dibuat\n/' $aha
sed -i '3s/^/! secara otomatis. Filter ini digunakan sebagai solusi untuk bug yang terdapat pada\n/' $aha
sed -i '4s/^/! AdGuard FiltersCompiler yang menyebabkan beberapa filter pada AdBlockID  dianggap\n/' $aha
sed -i '5s/^/! tidak valid, sehingga tidak bisa disalurkan pada AdGuard.\n/' $aha
sed -i '6s/^/!\n/' $aha
sed -i '7s/^/! Info lebih lanjut:\n/' $aha
sed -i '8s/^/! - https:\/\/github.com\/AdguardTeam\/FiltersRegistry\/issues\/259\n/' $aha
sed -i '9s/^/! - https:\/\/github.com\/AdguardTeam\/FiltersCompiler\/issues\/41\n/' $aha

sed -i '1s/^/!#if false\n/' $aha
sed -i '$s/$/\n!#endif/' $aha
