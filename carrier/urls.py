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


    # Tools
    # --------------------
    url(r'^fullTable/$', views.fullTable, name='fullTable'),
    url(r'^getFullTable/$', views.getFullTable, name='getFullTable'),


    # http://localhost/carriers/getUsersTravelMap/?date_init=2016-10-24T00:00:00&date_end=2017-01-25T00:00:00&_=1485262643655
    # {
    #   "3e4b1eda90e01f977577c4dbcad03091c76c33942b1217a7e7bbf6d2483e568a19f121a86562b5ac5e9da7ae8399da776e889c0f0b6a6961cc8ce61757e90f99": {
    #       "origin": {"latitude": -33.4459671, "timeStamp": "2016-12-14T12:22:13Z", "longitude": -70.6605514},
    #       "destination": {"latitude": -33.4461054, "timeStamp": "2016-12-14T13:21:14Z", "longitude": -70.6615643},
    #       "service": "418"
    #   },
    #   ...
    url(r'^getUsersTravelMap/$', views.getUsersTravelMap, name='getUsersTravelMap'),


    # http://localhost/carriers/getActiveUsers/?date=2016-10-24
    # {
    #   "half_hours": [
    #       {
    #           "half_hour": "2016-10-24 00:00:00-03:00 2016-10-25 00:29:59-03:00",
    #           "active_events": 1419,
    #           "active_users": 2,
    #           "reporting_users": 0,
    #           "reports": 0
    #       },
    #       ...
    # ]}
    url(r'^getActiveUsers/$', views.getActiveUsers, name='getActiveUsers'),



    # http://localhost/carriers/getUsersPositions/?date_init=2016-10-24T00:00:00&date_end=2017-01-25T00:00:00&_=1485262643655
    # {
    #   "9142b237-074c-4282-aaea-c586447087ac": [
    #       {"lat": -33.4382809, "timeStamp": "2016-10-26T22:17:45.363Z", "lon": -70.5732056},
    #       {"lat": -33.4391086, "timeStamp": "2016-10-26T22:18:22.036Z", "lon": -70.5726174},
    #       ...
    url(r'^getUsersPositions/$', views.getUsersPositions, name='getUsersPositions'),


    # http://localhost/carriers/getUsersActivities/?date_init=2016-10-24T00:00:00&date_end=2017-01-25T00:00:00&_=1485262643655
    # {
    #   "9142b237-074c-4282-aaea-c586447087ac": {
    #       "confirmBusCount": 0, "reportCount": 0, "declineBusStopCount": 0,
    #       "devicePositionInTimeCount": 45, "confirmBusStopCount": 0, "declineBusCount": 0,
    #       "busStopCheckCount": 54, "busEventCreationCount": 0, "tokenCount": 0, "busStopEventCreationCount": 0},
    #  "d4c4fe99-ee24-4d30-be2a-a4e032d0474b": {
    #       ...
    #  ...
    url(r'^getUsersActivities/$', views.getUsersActivities, name='getUsersActivities'),
]
