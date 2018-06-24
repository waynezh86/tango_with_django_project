import twstock
import datetime
import pytz
import csv


def determineEndDate(stock_date_tw, interval, offdays):

   base_date = stock_date_tw + datetime.timedelta(days = interval)
   
   end_date = base_date
   
   find_end_date = False
   
   while not find_end_date:
   
       # if the date is off day
   
       if end_date.weekday() >= 5 or datetime.datetime(end_date.year, end_date.month, end_date.day, 22, 0, tzinfo=pytz.timezone("Asia/Taipei")) in offdays:
	   
	       end_date = end_date + datetime.timedelta(days = 1)
		   
       else:
	   
	       find_end_date = True
		   
   return end_date

    
def determineLastOpenDate(stock_date_tw, offdays):
   
   last_date = stock_date_tw - datetime.timedelta(days = 1)
   
   find_last_date = False
   
   while not find_last_date:
   
       # if the date is off day
   
       if last_date.weekday() >= 5 or datetime.datetime(last_date.year, last_date.month, last_date.day, 22, 0, tzinfo=pytz.timezone("Asia/Taipei")) in offdays:
	   
	       last_date = last_date - datetime.timedelta(days = 1)
		   
       else:
	   
	       find_last_date = True
		   
   return last_date


   
   
   
#find the correct file where stock prices contained, and return pick-up date
#if current datetime is off-day or before 17pm, the stock_date is the last open day
#otherwise stock_date is today

def locateStockFile(tw_datetime, offdays, afternoon_start = 17, morning_end = 9):

    stock_date = tw_datetime.date()  #the date he made the bet
	
    if stock_date.weekday() >= 5 or datetime.datetime(stock_date.year, stock_date.month, stock_date.day, 22, 0, tzinfo=pytz.timezone("Asia/Taipei")) in offdays:
	
       last_date = determineLastOpenDate(stock_date, offdays)
       return 'stocks_' + str(last_date) + '.csv', last_date
	   

    if tw_datetime >= datetime.datetime(tw_datetime.year,tw_datetime.month,tw_datetime.day, afternoon_start,0, tzinfo=pytz.timezone("Asia/Taipei")):
       return 'stocks_' + str(tw_datetime.date()) + '.csv', stock_date
	   
    else:
       last_date = determineLastOpenDate(stock_date, offdays)
       return 'stocks_' + str(last_date) + '.csv', last_date


	   
def price_string(price):

   if price == None:
      return '此股票买入未成功'
   
   else:
      return '买入成功，价格为 NT${0}'.format(price)


def getCurrentPrice(code, localfetch = True, local = ''):


   if localfetch:
     
      price = None
      with open(local, 'r') as myfile:
       lines = csv.reader(myfile)
	   
       i = 0
       for line in lines:
	   
          if i == 0:
            i = i + 1
            continue
		
          else:
            if line[0] == code:
               if line[1] != 'None':
                 price = float(line[1])
               break
			     
      return price		   


	 
	 
	 
   #real time fetch --- suspend for now	 
   else:
     realtime_stk = twstock.realtime.get(code)
   
     if realtime_stk['success']:
       return float(realtime_stk['realtime']['latest_trade_price'])
   
     else:
       return None
	  
	  
def UTC_To_Taipei(a_utc_time):

   return a_utc_time.astimezone(pytz.timezone("Asia/Taipei"))

    