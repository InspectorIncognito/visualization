from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^carriers/', include('carrier.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login, name='login'),
]
