#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path
from django.urls import re_path
from django.urls.conf import include
from incoming.views import index, simple_page_not_found,\
        edit_detail_datain, outer, OuterXML
from rest_framework.routers import DefaultRouter,SimpleRouter
router = DefaultRouter()
router.register("xmlapi", OuterXML, basename="out")
app_name = 'incoming'
urlpatterns = [
    path('', edit_detail_datain, name='edit_datain'),
    re_path(r'^outer/.{36}/$', outer, name='to-payment'),
    re_path(r'pay-link/.{36}/$',outer, name='payments'),
    path('outxmldoc', OuterXML.as_view({'get':'xmlout'}), name='accept payment'),
    path('routa/', include(router.urls)),
]
handler404 = 'incoming.views.simple_page_not_found'
