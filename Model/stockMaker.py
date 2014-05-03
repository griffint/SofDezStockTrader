# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 21:06:38 2014

@author: griffin
"""


from stocks import *
from ystockquote.griffstockquote import *
import csv


#List of what row[number] relates to what field

#0=date
#1=company name
#2=ticker
#3=industry
#4=close
#5=volume


#def read_csv():
#    """
#    This function populates the database created in stocks.py with all
#    the data from the csv files we have
#    """
#    
#    with open('Tech500.csv', 'rb') as f:
#        reader = csv.reader(f)
#        reader.next()
#        for row in reader:
#            currentDate = row[1].split('/')
#            
#            if len(row)==len(filter(None, row)):
#                
#                db.session.add(Stock(row[0],date(int(currentDate[2]),int(currentDate[0]),int(currentDate[1])),row[2],row[3],row[4],row[5],float(row[6]),\
#                float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11])))    
#            else:pass
                
def database_from_internet():
    """Makes a new Datbase of the NYSE from the CSV and internet data"""
    with open('NYSEindustries.csv','rb') as f:
        reader = csv.reader(f)
        reader.next()
        tickersList = []
        next(reader)
        for row in reader:
            #first element of individual list will be ticker, then
            #company name, then
            tickersList.append([(row[1].split('/'))[0],(row[0].split('/'))[0],(row[4].split('/'))[0]])
        print tickersList
        #time to for loop through all our companies
        k=0
        for i in tickersList:
            print str(i[0])
            print i
            #now for each ticker we for loop through all data pulled from internet
            try:
                hist_dict = (get_historical_prices_list(str(i[0]),'2010-05-03','2014-05-03'))
            except:
                print "OOps, no data for this guy"
                continue
                
            volumes = hist_dict['Volume']
            dates = hist_dict['Date']
            prices = hist_dict['Price']
            for j in range(len(dates)):
                print k
                db.session.add(Stock(k,dates[j],i[1],i[0],\
                i[2],float(prices[j]),float(volumes[j])))
                k+=1
            
        
if __name__ == '__main__':
    
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")
    db.init_app(app)

    with app.app_context():

        db.create_all()
        database_from_internet()
        print "TIME TO COMMIT THE DATABASE"
        db.session.commit()