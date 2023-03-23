#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import django
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from incoming.models import CodeFunction, ProductionPurchase, MerchantData
from incoming.forms import ProductionPurchaseForm
from .serializers import CodeFunctionSerializer
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django import forms
from django.db import DatabaseError
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json, datetime
from django.http import Http404
import uuid
import re
from django.contrib.sites.models import Site
from django.template.response import TemplateResponse
import logging
LOGGER = logging.getLogger('django.request')


#not intended as view only utility function for building a large form
def get_insta_form(request):
    """utility function for building a large form"""
    LOGGER.debug('get instapay data:')
    m_site_name = "pleasetopmeup"
    m_site_reference = "cloud"
    m_card_allowed = "true"
    m_ieft_allowed = "true"
    m_mpass_allowed = "true"
    m_chips_allowed = "true"
    m_trident_allowed = "true"
    m_payat_allowed = "false"
    # buyer details
    match_result = request.path_info
    stripped_match = re.findall(r'/[a-zA-Z0-9-]{36}/', match_result)[-1]
    stripped_match = stripped_match.lstrip(r'/').rstrip(r'/')
    LOGGER.debug(stripped_match)
    try:
        buyer_details = ProductionPurchase.objects.filter(
            original_url_unique__pay_url=stripped_match)
    except DatabaseError as derr:
        LOGGER.debug(derr)
    LOGGER.debug(buyer_details)
    if (type(buyer_details) == list) or (type(buyer_details) == django.db.models.query.QuerySet):
        buyer_obj = buyer_details[0]
    else:
        LOGGER.debug('not a list')
        LOGGER.debug(str(type(buyer_details)))
        buyer_obj = buyer_details
    b_name = buyer_obj.name
    b_surname = buyer_obj.surname
    b_email = buyer_obj.email
    b_mobile = buyer_obj.mobile
    # get merchant_shortcode
    try:
        m_short = MerchantData.objects.get(pk=1)
    except DatabaseError as derr:
        LOGGER.debug(derr)
    if type(m_short) == list:
        merchant_data = m_short[0]
    else:
        merchant_data = m_short
    m_uuid = merchant_data.merchant_uuid
    m_account_uuid = merchant_data.merchant_account_uuid
    m_tx_order_nr = 'rhl' + str(uuid.uuid4())[-18:-1]
    m_tx_id = uuid.uuid4()  # spec in doc 36 chars/string len of 36
    m_tx_currency = 'ZAR'  # update to dynamic possibly later
    m_tx_amount = 0.00  # Decimal, total amount requested by buyer
    m_tx_item_name = 'Airtime'
    m_tx_item_description = 'prepaid'
    m_tx_invoice_nr = '00000'
    m_return_url = reverse('ussd:return-from-pay')
    m_cancel_url = reverse('ussd:cancel')
    m_pending_url = reverse('ussd:pending')
    m_notify_url = reverse('ussd:notify-after-paid')
    # m_email_address =
    # checksum
    jhttp_data = {'m_uuid': m_uuid, 'm_account_uuid': m_account_uuid, 'm_site_name': m_site_name,
                  'm_site_reference': m_site_reference, 'm_card_allowed': m_card_allowed,
                  'm_ieft_allowed': m_ieft_allowed, 'm_mpass_allowed': m_mpass_allowed,
                  'm_chips_allowed': m_chips_allowed, 'm_trident_allowed': m_trident_allowed,
                  'm_payat_allowed': m_payat_allowed, 'buyer_details': buyer_details, 'm_tx_order_nr': m_tx_order_nr,
                  'm_tx_id': m_tx_id, 'm_tx_currency': m_tx_currency,
                  'm_tx_amount': m_tx_amount, 'm_tx_item_name': m_tx_item_name,
                  'm_tx_item_description': m_tx_item_description,
                  'm_tx_invoice_nr': m_tx_invoice_nr, 'm_return_url': m_return_url,
                  'm_cancel_url': m_cancel_url, 'm_pending_url': m_pending_url, 'm_notify_url': m_notify_url,
                  'b_name': b_name, 'b_surname': b_surname, 'b_email': b_email, 'b_mobile': b_mobile,
                  }

    class InstaForm(forms.Form):
        f_m_uuid = forms.CharField(label='m_uuid', max_length=100)
        f_m_account_uuid = forms.CharField(label='m_account_uuid', max_length=100)

    insta_form_obj = InstaForm(initial=jhttp_data)
    return insta_form_obj

#ussd first phase
@csrf_exempt
def edit_detail_datain(request):
    """
    incoming json, outgoing xml??
    curl -k -X POST https://pleasetopmeup.com/ussdincoming -H 'Content-Type: application/json' -d '{"call_log":"256789506","amount":"39","user_number":"0792218349","sponsor_number":"0828000256","network":"Vodacom"}
    """
    LOGGER.debug(request.path_info)
    if request.method == 'GET':
        #LOGGER.debug("edit_detail_in:GET:" + str(request.__dict__))
        LOGGER.debug(request.content_params)
        LOGGER.debug(request._messages)
        t = TemplateResponse(request, 'incoming/home.html', {})
        return t
    elif request.method == 'POST':
        #post data received from logs:
        #b'{"call_log":"1011423848","amount":"56","user_number":"0792217404","sponsor_number":"0828000107","network":"Vodacom"}'
        #LOGGER.debug("edit_detail_in:POST" + str(request.__dict__))
        LOGGER.debug('POST')
        LOGGER.debug(request.path_info)
        LOGGER.debug(request.content_params)
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
        # http redirect to url serving xml doc
        # data was saved now return confirmation along with uuid
        LOGGER.debug('edit_detail_datain: phase1 complete')
        return OuterXML.as_view({'post': 'retrieve'})(request, pay_url=val_pay_url)
    else:
        LOGGER.debug('wrong method: GET')

#second phase
@csrf_protect
def outer(request):
    """
    unique url from request.
    start payment process debit card.
    """
    LOGGER.debug('outer:')
    if request.method == 'GET':
        LOGGER.debug('GET it now:')
        LOGGER.debug(request.GET.__dict__)
        LOGGER.debug(request.content_params)
        LOGGER.debug(request._messages)
        match_result = request.path_info
        stripped_match = re.findall(r'/[a-zA-Z0-9-]{36}/', match_result)[-1]
        stripped_match = stripped_match.lstrip(r'/').rstrip(r'/')
        LOGGER.debug(stripped_match)
        try:
            nr = CodeFunction.objects.get(pay_url=stripped_match)
            LOGGER.debug(nr)
            LOGGER.debug(nr.pay_url)
        except DatabaseError as e:
            LOGGER.debug('unable to retrieve entry')
            LOGGER.debug(e)
            raise Http404("cannot retrieve entry")
        
        try:
            jdomain = Site.objects.get_current().domain
        except DatabaseError as e:
            LOGGER.debug('unable to retrieve entry')
            LOGGER.debug(e)
            raise Http404("cannot retrieve entry")
        # use reverse and config in urls.py to 
        # call OuterXML restful interface detail method with arguments
        url_data = jdomain + reverse('incoming:out-detail', kwargs={'pay_url': nr.pay_url})
        LOGGER.debug(url_data)
        data_out = '<a href="https://{}">link text</a>'.format(url_data)
        LOGGER.debug(data_out)
        # use production purchase form and model to capture user info on request of unique url
        mob_nr = nr.sponsor_number
        form = ProductionPurchaseForm(initial={'mobile': mob_nr})
        context = {'form': form, 'data_something': data_out}
        LOGGER.debug(form.__dict__)
        return render(request, 'incoming/data_user.html', context)
    elif request.method == 'POST':
        LOGGER.debug('outer production purchase POST')
        LOGGER.debug(request.POST)
        form = ProductionPurchaseForm(request.POST)
        if form.is_valid():
            result = form.save()#Do lots of validation
            LOGGER.debug(result)
            # refresh result variable from db???
            match_result = request.path_info
            stripped_match = re.findall(r'/[a-zA-Z0-9-]{36}/', match_result)[-1]
            stripped_match = stripped_match.lstrip(r'/').rstrip(r'/')
            try:
                nr = CodeFunction.objects.get(pay_url=stripped_match)
                LOGGER.debug(nr)
                LOGGER.debug(nr.pay_url)
            except DatabaseError as e:
                LOGGER.debug('unable to retrieve entry')
                LOGGER.debug(e)
            result.original_url_unique = nr
            result.save()
            #next view to redirect to success page/instapay
            LOGGER.debug('redirecting to following url upon button press:')
            LOGGER.debug(reverse('ussd:to-instapay'))
            pay_url = reverse('ussd:to-instapay')
            pay_url = pay_url + '/' + stripped_match + '/'
            LOGGER.debug(pay_url)
            context = {'payment_destination': pay_url}
            LOGGER.debug('second phase complete')
            insta = get_insta_form(request)
            context.update({'insta': insta})
            return render(request, 'incoming/proceed_to_payment.html', context)
        else:
            new_form = ProductionPurchaseForm(request.POST)
            context = {'form': new_form}
            LOGGER.debug(context)
            return render(request, 'incoming/data_user.html', context)


# third phase
def pay_destination(request):
    if request.method == 'GET':
        LOGGER.debug('pay_destination:GET')
        #form redirects here from view named outer
        #gather data for instapay request and do redirect
        LOGGER.debug('redirecting')
        return HttpResponseRedirect(r'https://instapay-sandbox.trustlinkhosting.com/index.php')#redirect according to docs
    else:
        # not supported
        LOGGER.debug('pay_destination:Unsupported request')
        LOGGER.debug(request.method)


def pay_return(request):
    LOGGER.debug('pay_return')
    if request.method == 'GET':
        LOGGER.debug('GET')
        match_result = request.path_info
        stripped_match = re.findall(r'/[a-zA-Z0-9-]{36}/', match_result)[-1]
        stripped_match = stripped_match.lstrip(r'/').rstrip(r'/')
        LOGGER.debug(stripped_match)
    elif request.method == 'POST':
        LOGGER.debug('POST')
    else:
        LOGGER.debug('not supported')


def pay_notify(request):
    LOGGER.debug('pay_notify')
    if request.method == 'GET':
        LOGGER.debug('GET')
        match_result = request.path_info
        stripped_match = re.findall(r'/[a-zA-Z0-9-]{36}/', match_result)[-1]
        stripped_match = stripped_match.lstrip(r'/').rstrip(r'/')
        LOGGER.debug(stripped_match)
    elif request.method == 'POST':
        LOGGER.debug('POST')
    else:
        LOGGER.debug('not supported')


def pay_cancel(request):
    LOGGER.debug('pay_cancel')
    if request.method == 'GET':
        LOGGER.debug('GET')
        match_result = request.path_info
        stripped_match = re.findall(r'/[a-zA-Z0-9-]{36}/', match_result)[-1]
        stripped_match = stripped_match.lstrip(r'/').rstrip(r'/')
        LOGGER.debug(stripped_match)
    elif request.method == 'POST':
        LOGGER.debug('POST')
    else:
        LOGGER.debug('not supported')


def pay_pending(request):
    LOGGER.debug('pay_cancel')
    if request.method == 'GET':
        LOGGER.debug('GET')
        match_result = request.path_info
        stripped_match = re.findall(r'/[a-zA-Z0-9-]{36}/', match_result)[-1]
        stripped_match = stripped_match.lstrip(r'/').rstrip(r'/')
        LOGGER.debug(stripped_match)
    elif request.method == 'POST':
        LOGGER.debug('POST')
    else:
        LOGGER.debug('not supported')


def index(request):
    LOGGER.debug(request.GET)
    ingress_list = DataIn.objects.order_by('tag_name')[:5]
    context = {'ingress_list': ingress_list}
    return render(request, 'incoming/index.html', context)


def simple_page_not_found(request, exception):
    LOGGER.debug(request.GET)
    LOGGER.debug('simple page not found')
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

