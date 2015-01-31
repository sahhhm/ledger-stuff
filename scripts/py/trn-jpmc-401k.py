#!/usr/bin/env python
"""
Adhoc script to format 401K transactions to the ledger format.
The input parameter is passed as the last argument to the python invocation. Due
to the adhoc nature of this process, no checking is performed on the input.

The ledger transaction will be marked as "cleared".

The fund name will be processed to match my own naming standard (since none of
the 401k fund options are publicly listed). The naming standard currently in
use is the first letter of each word of the fund name (excluding the 500 for the
S&P500 Index) concatenated with a "_R" suffix.

Transaction types are currently limited to `Before-Tax`, `Roth 401(k)`, and
`Matching Contrib`.

Sample Call: 
------------
python trn-jpmc-401k.py path/to/input/data.dat

Sample Input: 
-------------
Each transaction appears on its own line, with each piece of transactional data
delimited by a tab `\t`

2015/01/30	Contributions	Before-Tax	Emerging Mrkt Eq Ix	$54.60	$8.92	6.1185
2015/01/30	Contributions	Before-Tax	Lg Cap Growth Index	$63.00	$16.40	3.8417

Sample Output:
--------------
2015/01/30 * EMEI_R Contributions
   ; :Contributions:
   Assets:Retirement:JPMC:401k:Trad  6.1185 EMEI_R @ $8.92
   Income:Paycheck:401k:Trad

2015/01/30 * LCGI_R Contributions
   ; :Contributions:
   Assets:Retirement:JPMC:401k:Trad  3.8417 LCGI_R @ $16.40
   Income:Paycheck:401k:Trad

"""

import sys

def process(input_file):
    delim = "   "
    assets = {"Before-Tax" : "Assets:Retirement:JPMC:401k:Trad",
              "Roth 401(k)" : "Assets:Retirement:JPMC:401k:Roth",
              "Matching Contrib" : "Assets:Retirement:JPMC:401k:Trad:Match"}
    
    incomes =  {"Before-Tax" : "Income:Paycheck:401k:Trad",
                "Roth 401(k)" : "Income:Paycheck:401k:Roth",
                "Matching Contrib" : "Income:Paycheck:401k:JPMCMatch"}


    with open(input_file, 'r') as f:

        for line in f.readlines():
            # 0 - Date
            # 1 - Action
            # 2 - Type
            # 3 - Fund
            # 4 - Total Price
            # 5 - Unit Price
            # 6 - Units
            s = [l.strip() for l in line.split('\t')]
            fund_name = format_fund(s[3])

            # "2015/01/30 * LCGI_R Contributions"
            print "{0} * {1} {2}".format(s[0], 
                                         fund_name,
                                         s[1])

            # "   ; :Contributions:"
            print "{0}; :{1}:".format(delim, 
                                      s[1])
            
            # "   Assets:Retirement:JPMC:401k:Trad  3.8417 LCGI_R @ $16.40"
            print "{0}{1}  {2} {3} @ {4}".format(delim,
                                                 assets[s[2]],
                                                 s[6],
                                                 fund_name,
                                                 s[5])
            
            # "   Income:Paycheck:401k:Trad"
            print "{0}{1}\n".format(delim,
                                    incomes[s[2]])


def format_fund(fund_name, suffix=None):
    if suffix == None:
        suffix = "_R"
    x = "".join([l[0] for l in fund_name.split() if l != "500"])
    return x + suffix

if __name__ == "__main__":
    process(sys.argv[-1])

