#!/bin/bash

readonly readme_template="vendor/readme/readme.template"
readonly readme_temp="vendor/readme/readme.tmp"

timestamp=`date -u +'%b %d, %Y'`
version=`date -u +'%y.%m.%d%H'`

# add to readme
sed -e "s/_timestamp_/$timestamp/g" -e "s/_version_/$version/g" $readme_template > $readme_temp

# add to file
cat $readme_temp > README.md
echo "- Adding Date"
echo "- Adding Version"

# remove tmp file
rm -rf $readme_temp
