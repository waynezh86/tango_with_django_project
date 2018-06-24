from django.contrib import admin

from goodadmin.models import UserProfile, Competition, StockPick


admin.site.register(UserProfile)
admin.site.register(Competition)
admin.site.register(StockPick)
