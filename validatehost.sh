#!/bin/bash

flrender -i abid=. tools/validatehost/host.template tools/validatehost/host.txt

python tools/validatehost/validatehost.py
