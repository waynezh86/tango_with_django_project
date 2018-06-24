from django.conf.urls import url

from goodadmin import views


urlpatterns = [
    url(r'^$', views.index, name = 'index'),
	url(r'^index/', views.index, name = 'index2'),
	url(r'^my_scores/', views.my_scores, name = 'RaceScore'),
	url(r'^race_status/', views.race_status, name = 'raceS'),
	url(r'^race_status_5days/', views.race_status_5days, name = 'raceS'),
	url(r'^face/', views.face, name = 'face'),
	url(r'^login_action/', views.login_action, name = 'login_act'),
    url(r'^register_action/', views.register_action, name = 'reg_act'),
    url(r'^logout_action/', views.logout_action, name = 'logout_act'),
	url(r'^pick_stocks/', views.pick_stocks, name = 'pick_stocks'),
	url(r'^pick_stocks_5days/', views.pick_stocks_5days, name = 'pick_stocks_5days'),
	url(r'^my_scores_5days/', views.my_scores_5days, name = 'my_scores_5days'),
]