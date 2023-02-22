#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from incoming.models import DataIn, FormalCellFind, CodeFunction
from .serializers import DataInSerializer, FormalCellFindSerializer
from django.http import HttpResponse
from django.db import DatabaseError
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from django.http import Http404

import logging
LOGGER = logging.getLogger('django.request')


class DataInListView(ListView):
    model = DataIn

class DataInDetailView(DetailView):
    model = DataIn


@csrf_exempt
def edit_detail_datain(request):
    """
    incoming json 
    """
    LOGGER.debug(request.path_info)
    if request.method == 'GET':
        #LOGGER.debug("edit_detail_in:GET:" + str(request.__dict__))
        LOGGER.debug(request.content_params)
        LOGGER.debug(request._messages)
        #save object to db
        val_call_log = request.GET['call_log']
        val_network = request.GET['network']
        val_amount = request.GET['amount']
        val_user_number = request.GET['user_number']
        val_sponsor_number = request.GET['sponsor_number']
        val_timestamp = datatime.datetime.now()
        try:
            fitem = CodeFunction(call_log=val_call_log, network=val_network, amount=val_amount,\
                    user_number=val_user_number, sponsor_number=val_sponsor_number,\
                    timestamp=val_timestamp)
            fitem.save()
        except DatabaseError:
            LOGGER.debug(DatabaseError)
            LOGGER.debug('Could not create entry')
            #404 cannot create

    elif request.method == 'POST':
        #post data received from logs:
        #b'{"call_log":"1011423848","amount":"56","user_number":"0792217404","sponsor_number":"0828000107","network":"Vodacom"}'
        LOGGER.debug("edit_detail_in:POST" + str(request.__dict__))
        LOGGER.debug('POST')
        LOGGER.debug(request.path_info)
        LOGGER.debug(request.content_params)
        LOGGER.debug(request.POST)
        LOGGER.debug(request.headers)
        LOGGER.debug('messages:')
        LOGGER.debug(request._messages)
        post_data_bytes = request.read()
        LOGGER.debug(post_data_bytes)
        post_data = post_data_bytes.decode('utf-8')
        pn = json.loads(post_data)
        LOGGER.debug(post_data)
        LOGGER.debug(pn)
        if pn.__contains__('call_log'):
            LOGGER.debug(pn['call_log'])
            val_call_log = pn['call_log']
        if pn.__contains__('amount'):
            val_amount = pn['amount']
        val_user_number = pn['user_number']
        val_sponsor_number = pn['sponsor_number']
        val_network = pn['network']
        val_timestamp = datetime.datetime.now()
        try:
            fitem = CodeFunction(call_log=val_call_log, network=val_network, amount=val_amount,\
                    user_number=val_user_number, sponsor_number=val_sponsor_number,\
                    timestamp=val_timestamp)
            fitem.save()
        except DatabaseError as e:
            LOGGER.debug('unable to create entry')
            LOGGER.debug(e)
            raise Http404("cannot create entry")
            #404 cannot create
    else:
        LOGGER.debug('bullshit GET')
    res = 'received ' + str(request.method) + '   -   ' + str(request.__dict__)
    return HttpResponse(res)

def index(request):
    LOGGER.debug(request.GET)
    ingress_list = DataIn.objects.order_by('tag_name')[:5]
    context = {'ingress_list': ingress_list}
    return render(request, 'incoming/index.html', context)

def simple_page_not_found(request, exception):
    LOGGER.debug(request.GET)
    return render(request, 'incoming/page_not_found.html')

from rest_framework import routers, serializers, viewsets
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response


class DataInViewSet(viewsets.ModelViewSet):
    queryset = DataIn.objects.all()
    serializer_class = DataInSerializer
    parser_classes = (XMLParser,)
    renderer_classes = (XMLRenderer,)
    
    def create(self, request):
        LOGGER.debug('create in DATAINVIEWSET')
        LOGGER.debug(request.method)
        super().create(request)

class FormalCellFindViewSet(viewsets.ModelViewSet):
    queryset = FormalCellFind.objects.all()
    serializer_class = FormalCellFindSerializer
    parser_classes = (XMLParser,)
    renderer_classes = (XMLRenderer,)
    
    def create(self, request):
        LOGGER.debug('create in FormalCellFindViewSet')
        LOGGER.debug(request.method)
        LOGGER.debug(request.path)
        super().create(request)




