# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 15:09:46 2014

@author: griffin
"""

from urllib2 import Request, urlopen
from urllib import urlencode

def _request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    req = Request(url)
    resp = urlopen(req)
    content = resp.read().decode().strip()
    return content
    
def get_company_name(symbol):
    return _request(symbol, 'n')
    
if __name__ == '__main__':
    print get_company_name('B')