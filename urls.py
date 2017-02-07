from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register ),
    url(r'^login$', views.login ),
    url(r'^quotes$', views.quotes, name = 'quotes' ),
    url(r'^additem$', views.additem ),
    url(r'^addingitem$', views.addingitem ),
    url(r'^joinninglist/(?P<id>\d+$)', views.joinninglist, name = 'joinninglist'),
    url(r'^users/(?P<id>\d+$)', views.users, name = 'users'),
    url(r'^removeitem/(?P<id>\d+$)', views.removeitem, name = 'removeitem'),
    url(r'^deleteitem/(?P<id>\d+$)', views.deleteitem, name = 'deleteitem'),
    url(r'^logoff$',views.logoff),


]
