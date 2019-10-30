#!/bin/bash

# Script ini digunakan untuk memperbarui versi dan tanggal perilisan AdBlockID
# pada file readme. Versi yang tertulis harus sama persis dengan yang tertulis
# pada ./output/adblockid.txt


readonly readme_template="tools/readme/readme.template"
readonly readme_tmp="tools/readme/readme.tmp"

v_mayor=`date -u +'%y'`
v_minor=`date -u +'%j'`
v_build=(`date -u +'%H'`*60)+`date -u +'%M'`
version=$((v_mayor)).$((v_minor)).$((v_build))

release_date=`date -u +'%b %d, %Y'`

# Buat file temporary
sed -e "s/_release_date_/$release_date UTC/g" -e "s/_version_/$version/g" $readme_template > $readme_tmp

# Ubah file temporary menjadi file readme yang sebenarnya
cat $readme_tmp > README.md
echo "- Adding Date"
echo "- Adding Version"

# Hapus file temporary
rm -rf $readme_tmp
