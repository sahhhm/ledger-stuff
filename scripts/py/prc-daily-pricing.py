#!/usr/bin/env python
"""
Adhoc program that will append current prices for a set of input commodities in
the standard ledger price format to the specified output file.

Sample call:
------------
python prc-daily-pricing.py a.out COMMA COMMB

Sample a.out contents:
----------------------
P 2014-11-12 16:00:00 COMMA $11.51
P 2014-11-12 16:01:00 COMMB $63.56

Thanks to https://github.com/cgoldberg/ystockquote for yahoo input mapping
"""

import argparse
import sys, datetime, time
from pprint import pprint
from urllib2 import Request, urlopen
   
def process(symbol, tags, labels, outf):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, tags)
    req = Request(url)
    resp = urlopen(req)    
    data = str(resp.read().decode('utf-8').strip().replace('"','')).split(',')
    res = dict(zip(labels,data))
    
    res['datetime'] = format_datetime(res['Last_Trade_Date'], res['Last_Trade_Time'])

    pprint(res)
    outf.write("P {datetime} {Symbol} ${Last_Trade_Price}\n".format(**res))
    
def format_datetime(a_date, a_time):
    td = a_date.split("/") # m/d/yyyy
    tt = a_time.split(":") # h:mm%p

    fmt = datetime.datetime.strptime("{} {} {} {} {} {}".format(
                                      td[2], td[0], td[1],
                                      tt[0], tt[1][0:2], tt[1][2:4]), "%Y %m %d %I %M %p")

    return fmt
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Command Line Stock Price\
                                                  Retrieval')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('a'),
                        default=sys.stdout)

    parser.add_argument('symbols', type=str, nargs='+', 
                        help='Comma separated list of symbols to look up')
                                                   
    args = parser.parse_args()
    tagsn = [('s', 'Symbol'), 
             ('l1', 'Last_Trade_Price'),
             ('c', 'Change'), 
             ('m', 'Day_Range'),
             ('d1', 'Last_Trade_Date'),
             ('t1', 'Last_Trade_Time'),

    ]    
    tags = "".join([item[0] for item in tagsn])
    labels = [item[1] for item in tagsn]    
    print args.outfile
    print args.symbols
    for symbol in args.symbols: 
        process(symbol, tags, labels, args.outfile)

