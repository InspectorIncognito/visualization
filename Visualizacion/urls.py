from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^data/', include('data.urls')),
    url(r'^admin/', admin.site.urls),
]
