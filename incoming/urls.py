#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path
from django.urls import re_path
from django.urls.conf import include
from incoming.views import simple_page_not_found,\
        edit_detail_datain, outer, OuterXML,\
        pay_return, pay_cancel, pay_pending,\
        InstaNotifyView, pay_notify_datain
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("xmlapi", OuterXML, basename="out")
app_name = 'incoming'
urlpatterns = [
    path('', edit_detail_datain, name='edit_datain'),
    path('jpay-notify-rest/<slug:ucode>/', InstaNotifyView.as_view(), name='notify-rest'),
    path('jpay-notify-rest/', InstaNotifyView.as_view(), name='notify-rest-get'),
    re_path(r'^index[.html]$', edit_detail_datain, name='edit_datain'),
    re_path(r'^outer/.{36}/$', outer, name='to-confirmation'),
    re_path(r'pay-link/.{36}/$', outer, name='payments'),
    re_path(r'jpay-return/$', pay_return, name='return-from-pay'),
    re_path(r'jpay-return/.{36}/$', pay_return, name='return-from-pay-post'),
    re_path(r'simple-jpay-return/$', pay_notify_datain, name='return-from-pay-simple'),
    re_path(r'simple-jpay-return/.{36}/$', pay_notify_datain, name='return-from-pay-simple-post'),
    re_path(r'jpay-cancel/$', pay_cancel, name='cancel'),
    re_path(r'jpay-cancel/.{36}/$', pay_cancel, name='cancel-post'),
    re_path(r'jpay-pending/$', pay_pending, name='pending'),
    re_path(r'jpay-pending/.{36}/$', pay_pending, name='pending-post'),
    path('routa/', include(router.urls)),
    path('404', simple_page_not_found, name='simple_page_not_found')]
handler404 = 'incoming.views.simple_page_not_found'
