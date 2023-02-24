#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path
from django.urls import re_path
from django.urls.conf import include
from incoming.views import index, simple_page_not_found, DataInListView,\
        edit_detail_datain, DataInDetailView, DataInViewSet,\
        FormalCellFindViewSet, outer, OuterXML
from rest_framework.routers import DefaultRouter,SimpleRouter
router = DefaultRouter()
router.register("xmlapi", OuterXML, basename="out")
app_name = 'incoming'
urlpatterns = [
    path('list_all/', DataInListView.as_view(), name='list_all_from_cell_network'),
    path('edit_datain', edit_detail_datain, name='edit_datain'),
    re_path('receiver/(?P<tag_name>.{1,100})', DataInDetailView.as_view(), name='insert_cell_request'),
    path('', edit_detail_datain, name='edit_datain'),
    #path('in', DataInViewSet.as_view({'get':'create', 'post':'create'}), name='ingress_ussd'),
    path('in', FormalCellFindViewSet.as_view({'get':'create', 'post':'create'}), name='ingress_ussd'),
    re_path(r'^outer/.{36}/$', outer, name='to-payment'),
    path('outxmldoc', OuterXML.as_view({'get':'xmlout'}), name='accept payment'),
    path('routa/', include(router.urls)),
]
handler404 = 'incoming.views.simple_page_not_found'
