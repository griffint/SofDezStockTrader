# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 21:06:38 2014

@author: griffin
"""


from stocks import *
import csv


#List of what row[number] relates to what field
#1=date
#2=company name
#3=ticker
#4=industry
#5=sector
#6=close
#7=high
#8=low
#9=daily trading volume
#10=short interest
#11=earnings per share

def read_csv():
    with open('Tech500.csv', 'rb') as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            currentDate = row[1].split('/')
            
            if len(row)==len(filter(None, row)):
                
                db.session.add(Stock(row[0],date(int(currentDate[2]),int(currentDate[0]),int(currentDate[1])),row[2],row[3],row[4],row[5],float(row[6]),\
                float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11])))    
             
    
if __name__ == '__main__':
    db.create_all()
    read_csv()
    db.session.commit()