from django.conf.urls import url
# , include
# from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    #  Sorted the same as in the dashboard

    # Dashboard homepage
    # --------------------
    url(r'^getCount/$', views.getCount, name='getCount'),


    # Drivers
    # --------------------

    # drivers events list
    url(r'^driversTable/$', views.driversTable, name='driversTable'),
    url(r'^getDriversTable/$', views.getDriversTable, name='getDriversTable'),

    # drivers events graph
    url(r'^drivers/$', views.drivers, name='drivers'),
    url(r'^getDriversData/$', views.getDriversReport, name='getDriversReport'),


    # Bus
    # --------------------

    # bus events lists
    url(r'^physicalTable/$', views.physicalTable, name='physicalTable'),
    url(r'^getPhysicalTable/$', views.getPhysicalTable, name='getPhysicalTable'),
    url(r'^updatePhysical/$', views.updatePhysical, name='updatePhysical'),
    url(r'^getPhysicalHeaders/$', views.getPhysicalHeaders, name='getPhysicalHeaders'),
    url(r'^getPhysicalData/$', views.getPhysicalReport, name='gePhysicalReport'),

    # bus events graph
    url(r'^physical/$', views.physical, name='physical'),

    # bus map
    url(r'^busMap/$', views.busMap, name='busMap'),
    url(r'^getBusMap/$', views.getBusMap, name='getBusMap'),
    url(r'^getBusMapParameters/$', views.getBusMapParameters, name='getBusMapParameters'),

    # bus reports
    url(r'^busReports/$', views.busReports, name='busReports'),
    url(r'^getBusReports/$', views.getBusReports, name='getBusReports'),

    # BusStop
    # --------------------

    # reports
    url(r'^busStopReports/$', views.busStopReports, name='busStopReports'),
    url(r'^getBusStopReports/$', views.getBusStopReports, name='getBusStopReports'),

    # bus stop events map
    url(r'^busStopMap/$', views.busStopMap, name='busStopMap'),
    url(r'^getBusStopInfo/$', views.getBusStopInfo, name='getBusStopInfo'),

    # User
    # --------------------

    # user activities
    url(r'^userActivities/$', views.userActivities, name='userActivities'),
    url(r'^getUsersActivities/$', views.getUsersActivities, name='getUsersActivities'),

    url(r'^activeUsers/$', views.activeUsers, name='activeUsers'),
    url(r'^getActiveUsers/$', views.getActiveUsers, name='getActiveUsers'),

    # bus stop views map
    url(r'^busStopViewsMap/$', views.busStopViewsMap, name='busStopViewsMap'),
    url(r'^getUsersPositions/$', views.getUsersPositions, name='getUsersPositions'),

    # user travels
    url(r'^usersTravelMap/$', views.usersTravelMap, name='usersTravelMap'),
    url(r'^getUsersTravelMap/$', views.getUsersTravelMap, name='getUsersTravelMap'),

    # Tools
    # --------------------
    url(r'^fullTableBus/$', views.fullTableBus, name='fullTableBus'),
    url(r'^getFullTableBus/$', views.getFullTableBus, name='getFullTableBus'),

    url(r'^fullTableStop/$', views.fullTableStop, name='fullTableStop'),
    url(r'^getFullTableStop/$', views.getFullTableStop, name='getFullTableStop'),

]
