from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime
from django.db import connection

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import realtime_stock
import pytz

# Create your models here.

class UserProfile(models.Model):
    
    #RegisterIP = models.CharField(max_length=128, unique = True)
    
	
    user = models.OneToOneField(User)
	
    def __str__(self):
     return self.user.username
	   
	   
class Competition(models.Model):
    CompID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    #CompID = models.IntegerField(primary_key=True, default = 0)
    StartDate = models.DateField()  #competition starting date (UTC DATE!!!!!!!!!!!)
    Interval = models.IntegerField(default = 0)  #pick time    
    EndDate = models.DateField()  #competition ending date     (UTC DATE!!!!!!!!!!!)
	
    def clean(self):
	   
       cursor = connection.cursor()
       cursor.execute("SELECT EndDate FROM goodadmin_Competition WHERE Interval = %s order by EndDate DESC limit 1", [self.Interval])
       result = cursor.fetchall()
	   
       utcdt = datetime.datetime.utcnow().replace(tzinfo = pytz.UTC)
       tw_datetime = utcdt.astimezone(pytz.timezone("Asia/Taipei"))
	   
       print(result)
       
       if self.StartDate <= result[0][0]:
           raise ValidationError(_('A similar competition is ongoing')) 

       if  self.StartDate < tw_datetime.date():
           raise ValidationError(_('Competition cannot start before today'))

       if  self.StartDate >= self.EndDate:
           raise ValidationError(_('Date is not right (start date is later than end date)')) 		   
	 
	 
    def __str__(self): 
     return str(self.CompID)
	 

class StockPick(models.Model):
    IDname = models.ForeignKey(User)
    CompID = models.ForeignKey(Competition)
    StockTicker = models.CharField(max_length=50)  # stock name picked
    StockCode = models.CharField(max_length=50,default = '0000')    # stock code picked
	
	
    PickDate = models.DateField(default=datetime.date.today())  # stock picking date, will be specified a TW date
    EndDate = models.DateField(default=datetime.date.today())   # the date when profit is calculated, also a TW date

    StockPickPrice = models.FloatField(default=0.0)  # stock price when picked
    StockEndPrice = models.FloatField(default=-1.0)  # stock price when competition end
    StockProfit = models.FloatField(default=0.0)  # stock profit in percentage
	
    def __str__(self): 
     return self.StockTicker + "#" + self.IDname.username + "#" + str(self.CompID)
	 















	 
	 
	 