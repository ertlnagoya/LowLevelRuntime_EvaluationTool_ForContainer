#!/bin/bash
curl -OL https://cve.mitre.org/data/downloads/allitems.csv
rm epss_scores*
curl -OL https://epss.cyentia.com/epss_scores-current.csv.gz
gunzip epss_scores*
mv epss_scores* epss_scores.csv
python3 tmp.py
