#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path
from django.urls import re_path

from incoming.views import index, simple_page_not_found, DataInListView,\
        edit_detail_datain, DataInDetailView, DataInViewSet,\
        FormalCellFindViewSet

app_name = 'incoming'
urlpatterns = [
    path('list_all/', DataInListView.as_view(), name='list_all_from_cell_network'),
    path('edit_datain', edit_detail_datain, name='edit_datain'),
    re_path('receiver/(?P<tag_name>.{1,100})', DataInDetailView.as_view(), name='insert_cell_request'),
    path('', edit_detail_datain, name='edit_datain'),
    #path('in', DataInViewSet.as_view({'get':'create', 'post':'create'}), name='ingress_ussd'),
    path('in', FormalCellFindViewSet.as_view({'get':'create', 'post':'create'}), name='ingress_ussd'),
]
handler404 = 'incoming.views.simple_page_not_found'
