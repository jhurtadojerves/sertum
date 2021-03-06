"""sertum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import login
from django.views.static import serve

from centro import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('centro.urls')),
    url(r'^', include('servicio.urls')),
    url(r'^', include('usuario.urls')),


    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT
    }),


    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    }, name='ver_imagen'),
]
