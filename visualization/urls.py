from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^carriers/', include('carrier.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
