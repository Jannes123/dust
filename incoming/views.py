#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import django
import hashlib
from decimal import *
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from incoming.models import CodeFunction, ProductionPurchase, MerchantData,\
    PayInit, PayBuyer
from incoming.forms import ProductionPurchaseForm
from .serializers import CodeFunctionSerializer, ExplicitPayInitSerializer
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django import forms
from django.db import DatabaseError
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
import json
import datetime
from django.http import Http404, HttpResponse
import uuid
import re
from django.contrib.sites.models import Site
from django.template.response import TemplateResponse
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, MultiPartParserError
from rest_framework import status
import logging
LOGGER = logging.getLogger('django.request')


#not intended as view only utility function for building a large form
def get_insta_form(request, jamount):
    """utility function for building a large form"""
    LOGGER.debug('get instapay data:')
    m_site_name = "pleasetopmeup"
    m_site_reference = "cloud"
    m_card_allowed = True
    m_ieft_allowed = True
    m_mpass_allowed = True
    m_chips_allowed = True
    m_trident_allowed = True
    m_payat_allowed = False
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
    # todo: revisit error conditions
    m_tx_amount = str(jamount)
    m_tx_amount_float = float(str(jamount))
    # format to currency amount
    m_tx_amount_for_checksum = ("{:,.2f}".format(m_tx_amount_float)).replace('.', '')
    LOGGER.debug(m_tx_amount_for_checksum)
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
    m_tx_item_name = 'Airtime'
    m_tx_item_description = 'prepaid'
    m_tx_invoice_nr = '{:06d}'.format(int(merchant_data.current_invoice_number))
    merchant_data.current_invoice_number = int(m_tx_invoice_nr) + 1
    try:
        merchant_data.save()
    except DatabaseError as save_err:
        LOGGER.debug(save_err)
    # build abs urls for instapay form
    try:
        jdomain = Site.objects.get_current().domain
    except DatabaseError as e:
        LOGGER.debug('get_insta_form: unable to retrieve entry')
        LOGGER.debug(e)
    m_return_url = 'https://' + jdomain + reverse('ussd:return-from-pay') + stripped_match + '/'
    m_cancel_url = 'https://' + jdomain + reverse('ussd:cancel') + stripped_match + '/'
    m_pending_url = 'https://' + jdomain + reverse('ussd:pending') + stripped_match + '/'
    #m_notify_url = 'https://' + jdomain + reverse('ussd:notify-rest-get') + stripped_match + '/'
    m_notify_url = 'https://' + jdomain + reverse('ussd:return-from-pay-simple') + stripped_match + '/'
    # m_email_address =
    # checksum
    LOGGER.debug("---sending checksum sending---")
    secret = 'c@!!@ll2023'
    check_calculation = "{}_{}_{}_{}_ZAR_{}"\
        .format(m_uuid, m_account_uuid, m_tx_id, m_tx_amount_for_checksum, secret)
    LOGGER.debug(check_calculation)
    check_calculation = check_calculation.encode('UTF-8', errors='strict')
    LOGGER.debug(check_calculation)
    check_calculation = hashlib.md5(check_calculation).hexdigest()
    LOGGER.debug(check_calculation)

    jhttp_data = {'m_uuid': m_uuid, 'm_account_uuid': m_account_uuid, 'm_site_name': m_site_name,
                  'm_site_reference': m_site_reference, 'm_card_allowed': m_card_allowed,
                  'm_ieft_allowed': m_ieft_allowed, 'm_mpass_allowed': m_mpass_allowed,
                  'm_chips_allowed': m_chips_allowed, 'm_trident_allowed': m_trident_allowed,
                  'm_payat_allowed': m_payat_allowed, 'm_tx_order_nr': m_tx_order_nr,
                  'm_tx_id': m_tx_id, 'm_tx_currency': m_tx_currency,
                  'm_tx_amount': m_tx_amount, 'm_tx_item_name': m_tx_item_name,
                  'm_tx_item_description': m_tx_item_description,
                  'm_tx_invoice_nr': m_tx_invoice_nr, 'm_return_url': m_return_url,
                  'm_cancel_url': m_cancel_url, 'm_pending_url': m_pending_url, 'm_notify_url': m_notify_url,
                  'b_name': b_name, 'b_surname': b_surname, 'b_email': b_email, 'b_mobile': b_mobile,
                  'checksum': check_calculation,
                  }

    class InstaForm(forms.Form):
        m_uuid = forms.CharField(label='m_uuid', max_length=100)
        m_account_uuid = forms.CharField(label='m_account_uuid', max_length=100)
        m_site_name = forms.CharField(label='m_site_name', max_length=100)
        m_site_reference = forms.CharField(label='m_site_reference', max_length=100)
        m_card_allowed = forms.BooleanField(label='m_card_allowed', required=False)
        m_ieft_allowed = forms.BooleanField(label='m_ieft_allowed', required=False)
        m_mpass_allowed = forms.BooleanField(label='m_mpass_allowed', required=False)
        m_chips_allowed = forms.BooleanField(label='m_chips_allowed', required=False)
        m_trident_allowed = forms.BooleanField(label='m_trident_allowed', required=False)
        m_payat_allowed = forms.BooleanField(label='m_payat_allowed', required=False)
        m_tx_order_nr = forms.CharField(label='m_tx_order_nr', max_length=100)
        m_tx_id = forms.CharField(label='m_tx_id', max_length=100)
        m_tx_currency = forms.CharField(label='m_tx_currency', max_length=100)
        m_tx_amount = forms.DecimalField(label='m_tx_amount')
        m_tx_item_name = forms.CharField(label='m_tx_item_name', max_length=100)
        m_tx_item_description = forms.CharField(label='m_tx_item_description', max_length=100, required=False)
        m_tx_invoice_nr = forms.CharField(label='m_tx_invoice_nr', max_length=100)
        m_return_url = forms.CharField(label='m_return_url', max_length=100)
        m_cancel_url = forms.CharField(label='m_cancel_url', max_length=100, required=False)
        m_pending_url = forms.CharField(label='m_pending_url', max_length=100, required=False)
        m_notify_url = forms.CharField(label='m_notify_url', max_length=100, required=False)
        b_name = forms.CharField(label='b_name', max_length=100, required=False)
        b_surname = forms.CharField(label='b_surname', max_length=100, required=False)
        b_email = forms.CharField(label='b_email', max_length=100)
        b_mobile = forms.CharField(label='b_mobile', max_length=100)
        checksum = forms.CharField(label='checksum', max_length=100)

    insta_form_obj = InstaForm(jhttp_data)
    LOGGER.debug('tried binding:')
    LOGGER.debug(insta_form_obj.is_bound)
    LOGGER.debug(insta_form_obj)

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
        amount = float(nr.amount)
        form = ProductionPurchaseForm(initial={'mobile': mob_nr, 'amnt': amount})
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
            context = {}
            LOGGER.debug('second phase complete')
            insta = get_insta_form(request, jamount=result.amount)
            context.update({'insta': insta})
            return render(request, 'incoming/proceed_to_payment.html', context)
        else:
            new_form = ProductionPurchaseForm(request.POST)
            context = {'form': new_form}
            LOGGER.debug(context)
            return render(request, 'incoming/data_user.html', context)


# third phase
def pay_return(request):
    LOGGER.debug('pay_return')
    if request.method == 'GET':
        LOGGER.debug('GET')
        match_result = request.path_info
        stripped_match = re.findall(r'/[a-zA-Z0-9-]{36}/', match_result)[-1]
        stripped_match = stripped_match.lstrip(r'/').rstrip(r'/')
        LOGGER.debug(stripped_match)
        context = {'home': reverse('ussd:edit_datain')}
        # todo:present payment and topup status
        return render(request, 'incoming/return.html', context)
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
    LOGGER.debug('pay_pending')
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
    ingress_list = PayInit.objects.all('tag_name')[:5]
    context = {'ingress_list': ingress_list}
    return render(request, 'incoming/index.html', context)


def dash(request):
    """dashboard displaying balances statuses etc."""
    if request.method == 'GET':
        # Fetching Balance
        import requests
        import xml.etree.ElementTree as ET
        url = "https://ws.freepaid.co.za/airtimeplus/"
        headers = {'content-type': 'text/xml'}
        body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:air="https://ws.freepaid.co.za/airtimeplus/">
           <soapenv:Header/>
           <soapenv:Body>
              <air:fetchBalance>
                 <request>
                    <user>{'5883139'}</user>
                    <pass>{'Free123'}</pass>
                 </request>
              </air:fetchBalance>
           </soapenv:Body>
        </soapenv:Envelope>
        """
        response = requests.post(url, data=body, headers=headers)
        root = ET.fromstring(response.text)

        balance = root.find(".//balance").text
        context = {'airtime_balance': balance}
        return render(request, 'incoming/dash.html', context)
    elif request.method == 'POST':
        LOGGER.debug('POST')
"""
from incoming import incomig_utils
incomig_utils.buy_airtime(2,'0792217404')
https://github.com/Jannes123/dialermaps/blob/master/maps/jutils.py  check cron setup for django
"""

def simple_page_not_found(request, exception):
    LOGGER.debug(request.GET)
    LOGGER.debug('simple page not found')
    return render(request, 'incoming/page_not_found.html')


class OuterXML(viewsets.ModelViewSet):
    queryset = CodeFunction.objects.all()
    serializer_class = CodeFunctionSerializer
    parser_classes = (XMLParser,)
    renderer_classes = (XMLRenderer,)
    lookup_field = 'pay_url'

    def xmlout(self, request, pay_url):
        LOGGER.debug('---found view---')
        #LOGGER.debug(kwargs)
        LOGGER.debug(request)
        #cashdrp = kwargs['pay_url']
        #queryset = self.get_queryset().filter(pay_url=cashdrp)
        doc_send = self.get_object()
        data_param = self.serializer_class(doc_send).data
        return Response(data_param, status=status.HTTP_200_OK)


class InstaNotifyView(APIView):
    """Save return data from instapay"""
    LOGGER.debug('Notify view class instance created')
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request, format=None):
        """
        Return a list of all notifications.
        """
        noties = [notify.payeeInvoiceNr for notify in PayInit.objects.all()]
        return Response(noties)

    @method_decorator(csrf_exempt)
    def post(self, request, ucode):
        """save PayInit PayBuyer PayRequest PayDetails"""
        LOGGER.debug(request)
        LOGGER.debug(request.content_type)
        LOGGER.debug(ucode)
        LOGGER.debug("post")
        serias = ExplicitPayInitSerializer(data=request.data)
        LOGGER.debug(serias.is_valid())
        if serias.is_valid():
            LOGGER.debug(serias.validated_data)
            LOGGER.debug('ser data is valid')
            LOGGER.debug(serias)
            try:
                serias.save()
            except DatabaseError as derr:
                LOGGER.debug(derr)
                # return
            LOGGER.debug(serias.data)
            return Response(status=status.HTTP_200_OK)
        else:
            LOGGER.debug('error: cannot save serializer')
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


@csrf_exempt
def pay_notify_datain(request):
    """
    incoming notification
    """
    LOGGER.debug(request.path_info)
    LOGGER.debug(request.method)
    if request.method == 'GET':
        LOGGER.debug("pay_botify:GET:" + str(request.__dict__))
        LOGGER.debug(request.content_params)
        LOGGER.debug(request._messages)
        LOGGER.debug('Not supported')
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    elif request.method == 'POST':
        #post data received from logs:
        #b'{}'
        LOGGER.debug("edit_detail_in:POST" + str(request.__dict__))
        LOGGER.debug(request.path_info)
        LOGGER.debug(request.content_params)
        post_data_bytes = request.read()
        LOGGER.debug(post_data_bytes)
        post_data = post_data_bytes.decode('utf-8')
        LOGGER.debug(post_data)
        notification = dict(x.split("=") for x in post_data.split("&"))#json.loads(post_data)
        LOGGER.debug(notification)
        LOGGER.debug(notification['payeeUuid'])
        payeeUuid = notification['payeeUuid']
        payeeAccountUuid = notification['payeeAccountUuid']
        payeeRefInfo = notification['payeeRefInfo']
        if 'payeeCategory1' in notification.keys():
            payeeCategory1 = notification['payeeCategory1']
        else:
            payeeCategory1 = ''
        if 'payeeCategory2' in notification.keys():
            payeeCategory2 = notification['payeeCategory2']
        else:
            payeeCategory2 = ''
        if 'payeeCategory3' in notification.keys():
            payeeCategory3 = notification['payeeCategory3']
        else:
            payeeCategory3 = ''
        if 'payeeSiteName' in notification.keys():
            payeeSiteName = notification['payeeSiteName']
        else:
            payeeSiteName = ''
        if 'payeeSiteReference' in notification.keys():
            payeeSiteReference = notification['payeeSiteReference']
        else:
            payeeSiteReference = ''
        payeeInvoiceNr = notification['payeeInvoiceNr']
        payeeOrderNr = notification['payeeOrderNr']
        payeeOrderItemName = notification['payeeOrderItemName']
        payeeOrderItemDescription = notification['payeeOrderItemDescription']

        try:
            pay_notification_entry_obj = PayInit(
                    payeeUuid=payeeUuid, payeeAccountUuid=payeeAccountUuid,
                    payeeRefInfo=payeeRefInfo, payeeCategory1=payeeCategory1, payeeCategory2=payeeCategory2,
                    payeeCategory3=payeeCategory3, payeeSiteName=payeeSiteName,
                    payeeSiteReference=payeeSiteReference, payeeInvoiceNr=payeeInvoiceNr,
                    payeeOrderNr=payeeOrderNr, payeeOrderItemName=payeeOrderItemName,
                    payeeOrderItemDescription=payeeOrderItemDescription
                    )
            pay_notification_entry_obj.save()
        except DatabaseError as e:
            LOGGER.debug('unable to create entry')
            LOGGER.debug(e)
            #raise Http404("cannot create entry")
            #404 cannot create
        # http redirect to url serving xml doc
        # data was saved now return confirmation along with uuid
        LOGGER.debug('notify: complete')
        LOGGER.debug('payeeRefInfo:'+str(payeeRefInfo))
        LOGGER.debug('must be equal to m_tx_order_nr')
        #return Response(status=status.HTTP_200_OK, content_type='application/x-www-form-urlencoded', data=None)
        return HttpResponse()
    else:

        LOGGER.debug('wrong method')
