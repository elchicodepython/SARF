#!/bin/bash

echo "Downloading templates from vulnrepo Github"

wget https://raw.githubusercontent.com/kac89/vulnrepo/master/src/assets/vulns.json -O assets/vulns.json

echo "Please run import_templates.py script to import them into SARF"
