#!/bin/bash

readonly abid="tools/dead-hosts/dead-hosts--AdBlockID_git_realodix.txt"

flrender -i abid=. tools/dead-hosts/dead-hosts.template $abid

sed -i '/^!/g' $abid
sed -i '/^#/g' $abid

sed -i '/^$/d' $abid
