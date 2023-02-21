#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from incoming.models import DataIn, FormalCellFind
from .serializers import DataInSerializer, FormalCellFindSerializer
from django.http import HttpResponse
from django.db import DatabaseError
from django.views.decorators.csrf import csrf_exempt

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
        val_msisdn = request.GET['msisdn']
        val_phase = request.GET['phase']
        val_sessionid = request.GET['sessionid']
        val_type = request.GET['type']
        val_networkid = request.GET['networkid']
        val_request = request.GET['request']
        try:
            fitem = FormalCellFind(msisdn=val_msisdn, phase=val_phase, jsessionid=val_sessionid,\
                    jtype=val_type, networkid=val_networkid,\
                    jrequest=val_request)
            fitem.save()
        except DatabaseError:
            LOGGER.debug(DatabaseError)
            LOGGER.debug('Could not create entry')
            #404 cannot create

    elif request.method == 'POST':
        LOGGER.debug("edit_detail_in:POST" + str(request.__dict__))
        LOGGER.debug('POST')
        LOGGER.debug(request.path_info)
        LOGGER.debug(request.content_params)
        LOGGER.debug(request.POST)
        LOGGER.debug(request.headers)
        LOGGER.debug(request._messages)
        if request.POST.__contains__('msisdn'):
            LOGGER.debug(request.POST['msisdn'])
            val_msisdn = request.POST['msisdn'][0]
        if request.POST.__contains__('phase'):
            val_phase = request.POST['phase'][0]
        val_sessionid = request.POST['sessionid'][0]
        val_type = request.POST['type'][0]
        val_networkid = request.POST['networkid'][0]
        val_request = request.POST['request'][0]
        try:
            fitem = FormalCellFind(msisdn=val_msisdn, phase=val_phase, jsessionid=val_sessionid,\
                    jtype=val_type, networkid=val_networkid,\
                    jrequest=val_request)
            fitem.save()
        except DatabaseError:
            LOGGER.debug(DatabaseError)
            LOGGER.debug('Could not create entry')
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




