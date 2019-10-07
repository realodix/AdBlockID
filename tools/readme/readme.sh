#!/bin/bash

readonly readme_template="tools/readme/readme.template"
readonly readme_temp="tools/readme/readme.tmp"

v_mayor=`date -u +'%y'`-17
v_minor=`date -u +'%j'`
version=$((v_mayor)).$((v_minor))`date -u +'.%H%M'`

release_date=`date -u +'%b %d, %Y'`

# Buat file temporary
sed -e "s/_release_date_/$release_date/g" -e "s/_version_/$version/g" $readme_template > $readme_temp

# Ubah file temporary menjadi file readme yang sebenarnya
cat $readme_temp > README.md
echo "- Adding Date"
echo "- Adding Version"

# Hapus file temporary
rm -rf $readme_temp
