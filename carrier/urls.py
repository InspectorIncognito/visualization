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
    url(r'^busMap/$', views.busMap, name='busMap'),
    url(r'^getBusMap/$', views.getBusMap, name='getBusMap'),
    url(r'^getBusMapParameters/$', views.getBusMapParameters, name='getBusMapParameters'),
    url(r'^usageRecords/$', views.usageRecords, name='usageRecords'),
    url(r'^usersActivities/$', views.usersActivities, name='usersActivities'),
    url(r'^getUsersActivities/$', views.getUsersActivities, name='getUsersActivities'),
    url(r'^getBusStopInfo/$', views.getBusStopInfo, name='getBusStopInfo'),
    url(r'^getUsersPositions/$', views.getUsersPositions, name='getUsersPositions'),
    url(r'^getActiveUsers/$', views.getActiveUsers, name='getActiveUsers'),
    url(r'^getUsersTravelMap/$', views.getUsersTravelMap, name='getUsersTravelMap'),
]
