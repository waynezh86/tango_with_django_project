from django.core.management.base import BaseCommand, CommandError
from goodadmin.models import User, Competition, StockPick

def populate():

   python_cat = add_cat('python')
   
   add_page(cat=python_cat, title = 'Official Python Tutorial', url = 'http://docs.python.org/2/tutorial/')
   add_page(cat=python_cat, title = 'How to Think like a Computer Scientist', url = 'http://www.greenteapress.com/thinkpython/')
   add_page(cat=python_cat, title = 'Learn Python in 10 Minutes', url = 'http://www.korokithakis.net/tutorials/python/')
   
   django_cat = add_cat("Django")
   
   add_page(cat= django_cat, title = "Official Django Tutorial", url = 'https://docs.djangoproject.com/en/1.5/intro/tutorial01/')
   add_page(cat= django_cat, title = "Django Rocks", url = 'http://www.djangorocks.com/')
   add_page(cat= django_cat, title = "How to Tango with Django", url = "http://www.tangowithdjango.com/")
   
   frame_cat = add_cat('Other Frameworks')
   add_page(cat= frame_cat, title = "Bottle", url = 'http://bottlepy.org/docs/dev/')
   add_page(cat= frame_cat, title = "Flask", url = 'http://flask.pocoo.org')


def add_user(IDname, title, url, views = 0):
   p = Page.objects.get_or_create(category = cat, title = title, url = url, views = views)[0]
   return p
   
def add_competition(name):
   c = Category.objects.get_or_create(name = name)[0]
   return c
   
def add_StockPick(name):
   c = Category.objects.get_or_create(name = name)[0]
   return c


class Command(BaseCommand):
   
   def handle(self, *args, **options):
     
     populate()