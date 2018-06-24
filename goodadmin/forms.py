from django import forms
from django.contrib.auth.models import User
from goodadmin.models import UserProfile
from goodadmin.models import StockPick


class UserForm(forms.ModelForm):
   
   class Meta:
       model = User
       fields = ('username', 'email', 'password')
       
   
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = () 
		
class StockForm(forms.ModelForm):
    class Meta:
        model = StockPick
        fields = ('StockTicker', 'StockCode') 



