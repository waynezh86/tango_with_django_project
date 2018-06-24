import csv
import datetime
import pytz

def read_offdays(fname):
    offdays = []

    with open(fname, 'r') as myfile:
  
     for l in myfile:
            #print(l)
            offdays.append(datetime.datetime.strptime(l.rstrip('\n'), '%Y-%m-%d %H:%M:%S').replace(tzinfo = pytz.timezone("Asia/Taipei")))

    return offdays
   
   
   

def read_stocklist(fname):

   stockinfos = {}

   with open(fname, 'r') as myfile:
     lines = csv.reader(myfile)
     
	 
     index = 0
     for l in lines:
       if index == 0:
            index += 1
            continue
       else:
          stockinfos[l[1]] = l
          index += 1
          #print(l)

   return stockinfos
   
   
def re_org_by_head(stockinfos):

   stk_groups = [[], [], [], [], [], [], [], [], [], []]
   
   
   for akey in sorted(stockinfos):
   
    
	
    stk_groups[int(akey[0])].append(stockinfos[akey])

   
   
   return stk_groups  
   
   
   