#!/bin/bash

README_TEMPLATE="vendor/readme/readme.template"
README_TEMP="vendor/readme/readme.tmp"

TIMESTAMP=`date -u +'%b %d, %Y'`
VERSION=`date -u +'%y.%m.%d%H'`

# add to readme
sed -e "s/_timestamp_/$TIMESTAMP/g" -e "s/_version_/$VERSION/g" $README_TEMPLATE > $README_TEMP

# add to file
cat $README_TEMP > README.md
echo "- Adding Date"
echo "- Adding Version"

# remove tmp file
rm -rf $README_TEMP
