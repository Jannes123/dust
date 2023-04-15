#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dust URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from dust import settings
admin.site.site_header = 'PTMU'
urlpatterns = [
        path('admin/', admin.site.urls),
        path('index.html', include('incoming.urls', namespace='index')),
        path('api-auth/', include('rest_framework.urls')),
        #path('data/', include('incoming.urls', namespace='data')),
        path('ussdincoming/', include('incoming.urls', namespace='ussd')),
        path('', include('incoming.urls', namespace='incoming')),
]
              #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
