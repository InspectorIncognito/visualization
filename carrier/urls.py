from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^drivers/$', views.drivers, name='drivers'),
    url(r'^physical/$', views.physical, name='physical'),
    url(r'^driversTable/$', views.driversTable, name='driversTable'),
    url(r'^getDriversData/$', views.getDriversReport, name='getDriversReport'),
    url(r'^getPhysicalData/$', views.getPhysicalReport, name='gePhysicalReport'),
    url(r'^getDriversTable/$', views.getDriversTable, name='getDriversTable'),
    url(r'^getFreeReport/$', views.getFreeReport, name='getFreeReport'),
    url(r'^getPhysicalHeader/$', views.getPhysicalHeaders, name='getPhysicalHeaders'),
]
