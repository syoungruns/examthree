from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^success$', views.success),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^add_quote$', views.add_quote),
	url(r'^destroy_quote/(?P<quote_id>\d+)$', views.destroy_quote),
	url(r'^users/(?P<user_id>\d+)$', views.users),
	url(r'^favs/(?P<quote_id>\d+)$', views.favs)
]
