#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path
from django.urls import re_path
from django.urls.conf import include
from incoming.views import index, simple_page_not_found,\
        edit_detail_datain, outer, OuterXML, pay_destination,\
        pay_return, pay_notify, pay_cancel, pay_pending
from rest_framework.routers import DefaultRouter, SimpleRouter
router = DefaultRouter()
router.register("xmlapi", OuterXML, basename="out")
app_name = 'incoming'
urlpatterns = [
    path('', edit_detail_datain, name='edit_datain'),
    re_path(r'^index[.html]$', edit_detail_datain, name='edit_datain'),
    re_path(r'^outer/.{36}/$', outer, name='to-confirmation'),
    re_path(r'^confirm$', pay_destination, name='to-instapay'),
    re_path(r'^confirm/.{36}/$', pay_destination, name='to-instapay-post'),
    re_path(r'pay-link/.{36}/$', outer, name='payments'),
    re_path(r'jpay-return/$', pay_return, name='return-from-pay'),
    re_path(r'jpay-return/[.{36}/]$', pay_return, name='return-from-pay-post'),
    re_path(r'jpay-notify/.{36}/$', pay_notify, name='notify-after-paid'),
    re_path(r'jpay-cancel/.{36}/$', pay_cancel, name='cancel'),
    re_path(r'jpay-pending/.{36}/$', pay_pending, name='pending'),
    path('outxmldoc', OuterXML.as_view({'get': 'xmlout'}), name='accept payment'),
    path('routa/', include(router.urls)),
    path('404', simple_page_not_found, name='simple_page_not_found')
]
handler404 = 'incoming.views.simple_page_not_found'
