from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<colorId>[1-7])/drivers/$', views.drivers, name='drivers'),
    url(r'^getDriversData/$', views.getDriversReportByInterval, name='driversReport'),
]
