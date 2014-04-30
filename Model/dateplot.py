# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 14:19:54 2014

@author: sawyer
"""

import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import MONDAY
from matplotlib.finance import quotes_historical_yahoo
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter

date2 = datetime.date.today()
timedelta = datetime.timedelta(4*365)
date1 = date2 - timedelta


# every monday
mondays   = WeekdayLocator(MONDAY)

# every 3rd month
months    = MonthLocator(range(1,13), bymonthday=1, interval=6)
monthsFmt = DateFormatter("%b '%y")


quotes = quotes_historical_yahoo('INTC', date1, date2)
if len(quotes) == 0:
    print ('Found no quotes')
    raise SystemExit

dates = [q[0] for q in quotes]
opens = [q[1] for q in quotes]

print dates
print dates[0]
print type(dates[0])

dates2 = []
for i in range(733777, 735353):
    dates2.append(i)
    
print len(dates)
print len(dates2)

fig, ax = plt.subplots()
ax.plot_date(dates2, opens, '-')
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
ax.xaxis.set_minor_locator(mondays)
ax.autoscale_view()
#ax.xaxis.grid(False, 'major')
#ax.xaxis.grid(True, 'minor')
ax.grid(True)

fig.autofmt_xdate()

plt.show()