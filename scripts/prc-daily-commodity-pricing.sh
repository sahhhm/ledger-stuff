#!/bin/bash

# Script to price all available ledger commodities.
# $1 - path to pricing file where output will be appended
# $COMMODITIES - list of commodities provided by ledger to price

ledger commodities > com.out

# remove retirement accounts (_R) because those funds are not publicly listed
# remove USD commoedity ($)
COMMODITIES=$(sed '/_R/d;/\$/d' com.out | tr "\\n" " ")

# execute daily pricing script with filtered list of commodities
python py/prc-daily-pricing.py $1 $COMMODITIES

rm -f com.out

