from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reports/$', views.reports, name='reports'),
    url(r'^getCount/$', views.getCount, name='getCount'),
    url(r'^drivers/$', views.drivers, name='drivers'),
    url(r'^physical/$', views.physical, name='physical'),
    url(r'^driversTable/$', views.driversTable, name='driversTable'),
    url(r'^physicalTable/$', views.physicalTable, name='physicalTable'),
    url(r'^getDriversData/$', views.getDriversReport, name='getDriversReport'),
    url(r'^getPhysicalData/$', views.getPhysicalReport, name='gePhysicalReport'),
    url(r'^getDriversTable/$', views.getDriversTable, name='getDriversTable'),
    url(r'^getPhysicalTable/$', views.getPhysicalTable, name='getPhysicalTable'),
    url(r'^getReports/$', views.getReports, name='getReports'),
    url(r'^getPhysicalHeaders/$', views.getPhysicalHeaders, name='getPhysicalHeaders'),
    url(r'^updatePhysical/$', views.updatePhysical, name='updatePhysical'),
    url(r'^fullTable/$', views.fullTable, name='fullTable'),
    url(r'^getFullTable/$', views.getFullTable, name='getFullTable'),
    url(r'^maptest/$', views.maptest, name='mapTest'),
    url(r'^getMap/$', views.getMap, name='getMap'),
]
