#!/bin/bash

# Script to price all available ledger commodities.

ledger commodities > com.out

# remove retirement accounts (_R) because those funds are not publicly listed
# remove USD commoedity ($)
COMMODITIES=$(sed '/_R/d;/\$/d' com.out | tr "\\n" " ")

# execute daily pricing script with filtered list of commodities
python py/prc-daily-pricing.py ~/ledger/prc/p.dat $COMMODITIES

rm -f com.out

