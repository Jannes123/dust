#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from incoming.models import CodeFunction
from .serializers import CodeFunctionSerializer
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.db import DatabaseError
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from django.http import Http404
import uuid
from django.contrib.sites.models import Site
import logging
LOGGER = logging.getLogger('django.request')


@csrf_exempt
def edit_detail_datain(request):
    """
    incoming json, outgoing xml?? 
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
        val_timestamp = datetime.datetime.now()
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
        #LOGGER.debug("edit_detail_in:POST" + str(request.__dict__))
        LOGGER.debug('POST')
        LOGGER.debug(request.path_info)
        LOGGER.debug(request.content_params)
        #LOGGER.debug(request.POST)
        #LOGGER.debug(request.headers)
        #LOGGER.debug('messages:')
        #LOGGER.debug(request._messages)
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
        val_pay_url = uuid.uuid1()
        try:
            fitem = CodeFunction(call_log=val_call_log, network=val_network, amount=val_amount,\
                    user_number=val_user_number, sponsor_number=val_sponsor_number,\
                    timestamp=val_timestamp, pay_url=val_pay_url)
            fitem.save()
        except DatabaseError as e:
            LOGGER.debug('unable to create entry')
            LOGGER.debug(e)
            raise Http404("cannot create entry")
            #404 cannot create
    else:
        LOGGER.debug('wrong method: GET')
    res = 'received ' + str(request.method)
    #http redirect to url serving xml doc
    LOGGER.debug('edit_detail_datain: phase1 complete')
    return OuterXML.as_view({'post':'retrieve'})(request, pay_url=val_pay_url)
    #return HttpResponse(res)


def outer(request):
    LOGGER.debug('outer:')
    if request.method == 'GET':
        LOGGER.debug('GET it now:')
        LOGGER.debug(request.content_params)
        LOGGER.debug(request._messages)
        match_result = request.path_info
        stripped_match = match_result.rstrip(r'/')
        LOGGER.debug(stripped_match)
        stripped_match = stripped_match.lstrip(r'/outer/')
        LOGGER.debug(stripped_match)
        nr = CodeFunction.objects.get(pay_url=stripped_match)
        LOGGER.debug(nr)
        LOGGER.debug(nr.pay_url)
        jdomain = Site.objects.get_current().domain
        url_data = jdomain + reverse('incoming:out-detail', kwargs={'pay_url':nr.pay_url})
        return HttpResponse(url_data)
    elif request.method == 'POST':
        LOGGER.debug('POST')
        return HttpResponse('Still busy...')


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
from rest_framework import status

class OuterXML(viewsets.ModelViewSet):
    queryset = CodeFunction.objects.all()
    serializer_class = CodeFunctionSerializer
    parser_classes = (XMLParser,)
    renderer_classes = (XMLRenderer,)
    lookup_field = 'pay_url'
    LOGGER.debug('outerxml modelviewset class')

    def xmlout(self, request, pay_url):
        LOGGER.debug('---found view---')
        #LOGGER.debug(kwargs)
        LOGGER.debug(request)
        #cashdrp = kwargs['pay_url']
        #queryset = self.get_queryset().filter(pay_url=cashdrp)
        doc_send = self.get_object()
        data_param = self.serializer_class(doc_send).data
        return Response(data_param, status=status.HTTP_200_OK)

