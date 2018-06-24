from django.shortcuts import render, render_to_response
from django.template import RequestContext
from goodadmin.models import User, Competition, StockPick
from goodadmin.forms import UserForm, UserProfileForm,StockForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.conf import settings
from django.contrib import messages

from realtime_stock import Talk2twStocks

import datetime
import pytz
import os

SELECT_STOCK_MSG_ACTIVE = '{0}日赛正在进行，请选股.'
SELECT_STOCK_MSG_INACTIVE = '最近的{0}日赛已经结束，暂时不能操作。请耐心等待下一次比赛开始。'

COMP_ACTIVE = '活跃'
COMP_ENDED = '结束'

def index(request):

  context = RequestContext(request)
  context_dict = {'username':request.user.username}
  

  
  if not request.user.is_authenticated():
    return HttpResponseRedirect("/goodadmin/login_action/")

  return render_to_response("goodadmin/index.html", context_dict, context)

  
def dashboardsales(request):

  context = RequestContext(request)
  
  
  context_dict = {}
  if not request.user.is_authenticated():
    return HttpResponseRedirect("/goodadmin/login_action/")
  
  
  
  return render_to_response("goodadmin/dashboard-sales.html", context_dict, context)

  
  
# get my picks at 5 day competititon  
def my_scores_5days(request):

  utcdt = datetime.datetime.utcnow().replace(tzinfo = pytz.UTC)
  tw_datetime = utcdt.astimezone(pytz.timezone("Asia/Taipei"))

  last_com = Competition.objects.filter(Interval = 5).order_by('EndDate').last()
  
  cursor = connection.cursor()
  cursor.execute("SELECT StockTicker, PickDate, StockPickPrice, EndDate, StockEndPrice, StockProfit, StockCode FROM goodadmin_StockPick where IDname_id in (SELECT id FROM auth_user where username = %s) and CompID_id in (SELECT CompID FROM goodadmin_Competition where Interval = 5 ORDER BY EndDate DESC limit 1)", [request.user.username])
  result = cursor.fetchall()
  print(type(result))
  
  allinfo = []
  index = 0  
  for pick in result:
     
     pick_l = list(pick)
	 
     if pick_l[4] < 0:
        pick_l[4] = '暂缺'
        pick_l[5] = '暂缺'
     allinfo.append(pick_l)

  context = RequestContext(request)
  
  if tw_datetime.date() > last_com.EndDate: status =  COMP_ENDED
  else: status = COMP_ACTIVE
  
  context_dict = {'username':request.user.username, 'allinfo':allinfo, 'startdt':last_com.StartDate, 'enddt':last_com.EndDate, 'comp_status': status}
  
  if not request.user.is_authenticated():
    return HttpResponseRedirect("/goodadmin/login_action/")
  
  
  
  return render_to_response("goodadmin/components-text-person-5days.html", context_dict, context)    
  
  
  
  
  
# get my picks at 1 day competititon
def my_scores(request):

  utcdt = datetime.datetime.utcnow().replace(tzinfo = pytz.UTC)
  tw_datetime = utcdt.astimezone(pytz.timezone("Asia/Taipei"))

  last_com = Competition.objects.filter(Interval = 1).order_by('EndDate').last()
  
  cursor = connection.cursor()
  cursor.execute("SELECT StockTicker, PickDate, StockPickPrice, EndDate, StockEndPrice, StockProfit, StockCode FROM goodadmin_StockPick where IDname_id in (SELECT id FROM auth_user where username = %s) and CompID_id in (SELECT CompID FROM goodadmin_Competition where Interval = 1 ORDER BY EndDate DESC limit 1)", [request.user.username])
  result = cursor.fetchall()
  print(type(result))
  
  allinfo = []
  index = 0  
  for pick in result:
     
     pick_l = list(pick)
	 
     if pick_l[4] < 0:
        pick_l[4] = '暂缺'
        pick_l[5] = '暂缺'
     allinfo.append(pick_l)

  context = RequestContext(request)
  
  if tw_datetime.date() > last_com.EndDate: status =  COMP_ENDED
  else: status = COMP_ACTIVE
  
  context_dict = {'username':request.user.username, 'allinfo':allinfo, 'startdt':last_com.StartDate, 'enddt':last_com.EndDate, 'comp_status': status}
  
  if not request.user.is_authenticated():
    return HttpResponseRedirect("/goodadmin/login_action/")
  
  
  
  return render_to_response("goodadmin/components-text-person.html", context_dict, context)  

def face(request):

  context = RequestContext(request)
  
  
  context_dict = {}
  
  if not request.user.is_authenticated():
    return HttpResponseRedirect("/goodadmin/login_action/")
  
  
  
  return render_to_response("goodadmin/landing_index.html", context_dict, context) 


  # pick stock and store them  --- 5days
def pick_stocks_5days(request):

  if not request.user.is_authenticated():
  
    return HttpResponseRedirect("/goodadmin/login_action/")
  

  cursor = connection.cursor()
  cursor.execute("SELECT CompID, EndDate FROM goodadmin_Competition where Interval = 5 ORDER BY EndDate DESC limit 1")
  result = cursor.fetchall()

  context = RequestContext(request)
  utcdt = datetime.datetime.utcnow().replace(tzinfo = pytz.UTC)
  tw_datetime = utcdt.astimezone(pytz.timezone("Asia/Taipei"))
  
  #figure out if today has passed due day
  
  context_dict = {'stocks':settings.STOCKS_OD}
  
  if tw_datetime.date() > result[0][1]:
     context_dict['msg'] = [SELECT_STOCK_MSG_INACTIVE.format(5), 'danger', 'disabled']
    
  
  
  if request.method == 'GET':
    return render_to_response("goodadmin/stocks_list_5days.html", context_dict, context)

  else:
    stk_se = request.POST.getlist('stock_check')
	
    print('stk_se')
    print(stk_se)
	
    save_success = []
	
    for stock_info in stk_se:
	  
      print(stock_info)
      stock = stock_info[(stock_info.find('(') + 1):stock_info.find(')')]
	
      stock_file, stock_dt = Talk2twStocks.locateStockFile(tw_datetime, settings.OFFDAYS)	  
      stk_price = Talk2twStocks.getCurrentPrice(stock, local = os.path.join(settings.BASE_DIR, 'static', 'goodadmin', stock_file))
	  
      if stk_price == None:
         save_success.append([stock_info, Talk2twStocks.price_string(stk_price)])
         continue
	
      formdata = {'StockCode': stock, 'StockTicker': settings.ALL_STOCKS[stock][2]}
      pick_form = StockForm(data = formdata)
      pick = pick_form.save(commit=False)
      pick.IDname = User.objects.get(username = request.user.username)
      pick.CompID = Competition.objects.filter(Interval = 5).order_by('EndDate').last()
      pick.StockPickPrice = stk_price
	  
      pick.PickDate = stock_dt
	  
      
      pick.EndDate = Talk2twStocks.determineEndDate(stock_dt, 5, settings.OFFDAYS)
	  
	  
      print(pick.StockPickPrice)
	  
      pick.save()
      print('save is successful')
	  
      save_success.append([stock_info, Talk2twStocks.price_string(stk_price)])
    
    context_dict['save_success'] = save_success
    return render_to_response("goodadmin/stocks_list_5days.html", context_dict, context)

	

# pick stock and store them  --- 1 day
def pick_stocks(request):

  cursor = connection.cursor()
  cursor.execute("SELECT CompID, EndDate FROM goodadmin_Competition where Interval = 1 ORDER BY EndDate DESC limit 1")
  result = cursor.fetchall()

  context = RequestContext(request)
  utcdt = datetime.datetime.utcnow().replace(tzinfo = pytz.UTC)
  tw_datetime = utcdt.astimezone(pytz.timezone("Asia/Taipei"))
  
  #figure out if today has passed due day
  
  context_dict = {'stocks':settings.STOCKS_OD}
  
  if tw_datetime.date() > result[0][1]:
     context_dict['msg'] = [SELECT_STOCK_MSG_INACTIVE.format(1), 'danger', 'disabled']
  
  
 
    
  if not request.user.is_authenticated():
  
    return HttpResponseRedirect("/goodadmin/login_action/")
  
  
  if request.method == 'GET':
    return render_to_response("goodadmin/stocks_list.html", context_dict, context)

  else:
    stk_se = request.POST.getlist('stock_check')
	
    print('stk_se')
    print(stk_se)
    save_success = []
	
    for stock_info in stk_se:
	  
      print(stock_info)
      stock = stock_info[(stock_info.find('(') + 1):stock_info.find(')')]
	
      stock_file, stock_dt = Talk2twStocks.locateStockFile(tw_datetime, settings.OFFDAYS)	  
      stk_price = Talk2twStocks.getCurrentPrice(stock, local = os.path.join(settings.BASE_DIR, 'static', 'goodadmin', stock_file))
	  
      if stk_price == None:
        save_success.append([stock_info, Talk2twStocks.price_string(stk_price)])
        continue
	
      formdata = {'StockCode': stock, 'StockTicker': settings.ALL_STOCKS[stock][2]}
      pick_form = StockForm(data = formdata)
      pick = pick_form.save(commit=False)
      pick.IDname = User.objects.get(username = request.user.username)
      pick.CompID = Competition.objects.filter(Interval = 1).order_by('EndDate').last()
      pick.StockPickPrice = stk_price
	  
      pick.PickDate = stock_dt
	  
      
      pick.EndDate = Talk2twStocks.determineEndDate(stock_dt, 1, settings.OFFDAYS)
	  
	  
      print(pick.StockPickPrice)
	  
      pick.save()
      print('save is successful')
	  
      save_success.append([stock_info, Talk2twStocks.price_string(stk_price)])
    
    context_dict['save_success'] = save_success
    return render_to_response("goodadmin/stocks_list.html", context_dict, context)  
  
  
  
  
#default,  1 day competititon ranking
def race_status(request):

  utcdt = datetime.datetime.utcnow().replace(tzinfo = pytz.UTC)
  tw_datetime = utcdt.astimezone(pytz.timezone("Asia/Taipei"))

  last_com = Competition.objects.filter(Interval = 1).order_by('EndDate').last()

  if not request.user.is_authenticated():
    return HttpResponseRedirect("/goodadmin/login_action/")

  context = RequestContext(request)
  
  cursor = connection.cursor()
  cursor.execute("SELECT IDname_id, COUNT(IDname_id) as picktimes, AVG(StockProfit) as avg_profit FROM goodadmin_StockPick where CompID_id in (SELECT CompID FROM goodadmin_Competition where Interval = 1 ORDER BY EndDate DESC limit 1) GROUP BY IDname_id ORDER BY avg_profit DESC")
  result = cursor.fetchall()
  
  print('race 1 day')
  print(result)
  print(type(result))
  
  
  
  #top 10
  if len(result) >= 10:
    topN = result[:10]
  else:
    topN = result
	
	
  allinfo = []

  rank = 1
  for x in topN:

    allinfo.append([x, User.objects.get(id = x[0]).username, rank])
    rank = rank+1
      
  print(allinfo)
  if tw_datetime.date() > last_com.EndDate: status =  COMP_ENDED
  else: status = COMP_ACTIVE
  
  context_dict = {'allinfo': allinfo, 'username':request.user.username,'startdt':last_com.StartDate, 'enddt':last_com.EndDate, 'comp_status': status}
  
  
   
  return render_to_response("goodadmin/components-text.html", context_dict, context)


  
#5 days competititon  ranking
def race_status_5days(request):

  if not request.user.is_authenticated():
    return HttpResponseRedirect("/goodadmin/login_action/")
	
  utcdt = datetime.datetime.utcnow().replace(tzinfo = pytz.UTC)
  tw_datetime = utcdt.astimezone(pytz.timezone("Asia/Taipei"))

  last_com = Competition.objects.filter(Interval = 5).order_by('EndDate').last()
	
  context = RequestContext(request)
  
  cursor = connection.cursor()
  cursor.execute("SELECT IDname_id, COUNT(IDname_id) as picktimes, AVG(StockProfit) as avg_profit FROM goodadmin_StockPick where CompID_id in (SELECT CompID FROM goodadmin_Competition where Interval = 5 ORDER BY EndDate DESC limit 1) GROUP BY IDname_id ORDER BY avg_profit DESC")
  result = cursor.fetchall()
  
  print('race 5 day')
  print(result)
  print(type(result))
  
  
  
  #top 10
  if len(result) >= 10:
    topN = result[:10]
  else:
    topN = result
	
	
  allinfo = []

  rank = 1
  for x in topN:

    allinfo.append([x, User.objects.get(id = x[0]).username, rank])
    rank = rank + 1

      
  print(allinfo)
  
  if tw_datetime.date() > last_com.EndDate: status =  COMP_ENDED
  else: status = COMP_ACTIVE
  context_dict = {'allinfo': allinfo, 'username':request.user.username,'startdt':last_com.StartDate, 'enddt':last_com.EndDate, 'comp_status': status}
  
  
   
  return render_to_response("goodadmin/components-text-5days.html", context_dict, context)
  







  
################################################### Register & Sign UP #######################################################  
  
  
  
def register_action(request):

   registered = False
   usershow = ''

   if request.method == 'POST':
        
       formdata = {'username': request.POST.get('form-your-id'), 'email': request.POST.get('form-email'), 'password':request.POST.get('form-password')}
       a_user_form = UserForm(data = formdata)
       a_userp_form =  UserProfileForm(data = {})      
       
       print('before validate')
       
       if a_user_form.is_valid():
	   
           user = a_user_form.save()
           user.set_password(formdata['password'])
           user.save()
           usershow = request.POST.get('form-your-id')
           
           
           profile = a_userp_form.save(commit=False)
           profile.user = user
           
           profile.save()
           
		   
           registered = True
           
           user2 = authenticate(username=formdata['username'], password=formdata['password'])  #authenticate user
           if user2:		
             if user2.is_active:
		   
               login(request, user2)
       
       else:
	       print(a_user_form.errors)
		   
   else: 
       return render_to_response("goodadmin/login_register.html", {}, RequestContext(request))
	
   if registered:
   
     print('if registered')
     context = RequestContext(request)
     context_dict = {'username':usershow}
     
     
     return HttpResponseRedirect("/goodadmin/index/")

   else:
     context = RequestContext(request)
     context_dict = {}   
     return render_to_response("goodadmin/login_register.html", context_dict, context) 
	

	
	
def login_action(request):

   context = RequestContext(request)
   context_dict = {}

   if request.method == 'POST':
      
        username = request.POST.get('form-username')
        password = request.POST.get('form-password')
		
        user = authenticate(username=username, password=password)
		
        if user:		
           if user.is_active:
		   
             login(request, user)
			 
             return HttpResponseRedirect("/goodadmin/index/")
           else:
             return HttpResponseRedirect("/goodadmin/login_action/")
		
		
        else:
          return HttpResponseRedirect("/goodadmin/login_action/")
		
   else:
       return render_to_response("goodadmin/login_register.html", context_dict, context) 	
		

def logout_action(request):

   logout(request)
   return HttpResponseRedirect("/goodadmin/login_action/")   
		
		
		
		
  
  
  