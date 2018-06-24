from django.core.management.base import BaseCommand, CommandError
from goodadmin.models import User, Competition, StockPick
from realtime_stock import Talk2twStocks
from django.db import connection
from django.conf import settings
import datetime
import twstock
import csv
from goodadmin_fileloader import load_stocks
import time
import win_unicode_console
from realtime_stock import Talk2twStocks
import pytz
import os

win_unicode_console.enable()


def debug_twstock():

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM goodadmin_StockPick ')
    all_records = cursor.fetchall()
	
    for res_row in all_records:
	
      if res_row[0] == 1:
        print(res_row[8])
        print(res_row[8] == datetime.date(2018,6,16))
	  
      print(res_row)
   


#download the latest stock price

def download_today_prices():

   gupiao_path = os.path.join(settings.BASE_DIR, 'static', 'goodadmin', 'gupiao.csv')
   
   stock_cache = {}
   #slist = load_stocks.read_stocklist('C:\\Study\\HTC\\Django\\tango_with_django_project\\static\\goodadmin\\gupiao.csv')
   print(gupiao_path)
   slist = load_stocks.read_stocklist(gupiao_path)
   tday = datetime.datetime.utcnow().replace(tzinfo = pytz.UTC)
   tday_tw = Talk2twStocks.UTC_To_Taipei(tday)
   
   print(tday_tw)
   
   stock_price_path = os.path.join(settings.BASE_DIR, 'static', 'goodadmin', 'stocks_' + str(tday_tw.date()) + '.csv')
   
   stock_file = open(stock_price_path, 'w', newline = '')
   stock_writer = csv.writer(stock_file)
   stock_writer.writerow(['code', 'price'])
   
   failcount = 0
   
   for scode in slist:
     print('{0} processing...'.format(scode))
	 
     try:	  
	  
      rt_stock = twstock.Stock(scode, initial_fetch = False)
      rt_stock.fetch_from(tday.year, tday.month)
      time.sleep(1)
	  
      if rt_stock.close is not None and len(rt_stock.close) != 0:
        p = rt_stock.close[-1]
        stock_writer.writerow([scode, str(p)])
        stock_cache[scode] = p
        print(str(p))
      else:
        print('fails')
        failcount = failcount + 1
	 
     except Exception:
       print('something wrong happend with {0}'.format(scode))
       continue	   
     
		 
   print('fail num {0}'.format(failcount))
   
   stock_file.close()
   return stock_cache, tday_tw


# populate the end price of stock, and computer profit rate
def populate_db(stock_cache, tday_tw):


   cursor = connection.cursor()
   cursor.execute("SELECT goodadmin_StockPick.id, goodadmin_StockPick.StockTicker, goodadmin_Competition.Interval, goodadmin_StockPick.PickDate, goodadmin_StockPick.StockCode, goodadmin_StockPick.StockPickPrice， goodadmin_StockPick.EndDate FROM goodadmin_StockPick inner join goodadmin_Competition on goodadmin_StockPick.CompID_id = goodadmin_Competition.CompID where StockEndPrice < 0")

   result = cursor.fetchall()
   
   

   for record in result:
   
   
      if tday_tw.date() != record[6]: continue     #if today is not end date of the stock
      
      endprice = None
      if record[4] not in stock_cache:                  #if stock not fetched successfully
         pass     
      else:                                             #if stock fetched earlier
         endprice = stock_cache[record[4]]

      print(endprice)
 
      update_cmd = "UPDATE goodadmin_StockPick SET StockEndPrice = %s, StockProfit = %s WHERE id = %s"
      cursor.execute(update_cmd, [endprice, (endprice - record[5])/record[5], record[0]])
	     
   
def populate_cache():
      
       interval_to_path = {1:'', 5:''}

       cursor = connection.cursor()
	   
       for x in interval_to_path.keys():
         print(x)
         cursor.execute('SELECT CompID FROM goodadmin_Competition where Interval = %s', [x])
         all_ids = cursor.fetchall()

         print(all_ids)
         print(type(all_ids[0]))		 
	   
         for id in all_ids:
           cursor.execute("SELECT IDname_id, AVG(StockProfit) as avg_profit, COUNT(IDname_id) as picktimes FROM goodadmin_StockPick where CompID_id = %s GROUP BY IDname_id ORDER BY avg_profit DESC", [id[0]])
           result = cursor.fetchall()
		   
           comp_file = open(id[0] + '.csv', 'w')
           comp_writer = csv.writer(comp_file)
           
           for res_row in result:
               comp_writer.writerow(res_row)

           comp_file.close()			   
      
	  

   



class Command(BaseCommand):
   
   def handle(self, *args, **options):
     
     #populate_db()
     #populate_cache()
     #debug_twstock()
     stock_cache,tday_tw = download_today_prices()
     populate_db(stock_cache, tday_tw)
	 
	 
	 
	 
	 
	 
	 
	 
	 
	 
	 
	 