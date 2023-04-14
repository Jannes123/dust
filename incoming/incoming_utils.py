#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django_cron import CronJobBase, Schedule
from incoming.models import ProcessingPurchase
from django.db import DatabaseError
import requests
import xml.etree.ElementTree as ET
import json
import sys

import logging
LOGGER = logging.getLogger('django.request')
LOGGER.debug(sys.path)

freepd_error_codes = [("airtimeOKAY", "000"),
                      ("airtimePENDING", "001"),
                      ("airtimeEMPTYORDER", "100"),
                      ("airtimeINVALIDUSER", "101"),
                      ("airtimeINVALIDLAST", "102"),
                      ("airtimeINVALIDPASS", "103"),
                      ("airtimeINVALIDNETWORK", "104"),
                      ("airtimeINVALIDSELLVALUE", "105"),
                      ("airtimeFUNDSEXCEEDED", "106"),
                      ("airtimeOUTOFSTOCK", "107"),
                      ("airtimeINVALIDCOUNT", "108"),
                      ("airtimeINVALIDREFNO", "109"),
                      ("airtimeINVALIDREQUEST", "110"),
                      ("airtimeSTILLBUSY", "111"),
                      ("airtimeINVALIDORDERNUMBER", "112"),
                      ("airtimeINVALIDEXTRA", "113"),
                      ("airtimeINTERNAL", "197"),
                      ("airtimeTEMPORARY", "198"),
                      ("airtimeUNKNOWN", "199")
                      ]


def report_on_airtime(order_number):
    LOGGER.debug('report on airtime:' + str(order_number))
    url = "https://ws.freepaid.co.za/airtimeplus/"
    headers = {'content-type': 'text/xml'}
    body = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:air="https://ws.freepaid.co.za/airtimeplus/">
       <soapenv:Header/>
       <soapenv:Body>
          <air:queryOrder>
             <request>
                <user>{'5883139'}</user>
                <pass>{'Free123'}</pass>
                <orderno>{'{order_number}'}</orderno>
             </request>
          </air:queryOrder>
       </soapenv:Body>
    </soapenv:Envelope>
    """.format(order_number=order_number)

    response = requests.post(url, data=body, headers=headers)
    root = ET.fromstring(response.text)
    LOGGER.debug(root)
    # print(response.text)
    error_code = root.find(".//errorcode").text
    LOGGER.debug('error_code:')
    LOGGER.debug(error_code)
    order_status = root.find(".//status").text
    data = {"error_code": error_code}
    return data


def buy_airtime(amount, destination, network):
    """
    :@param amount: topup amount on user account.
    :@param destination: cell phone nr of initiating user
    :@param network: cell network designation Voda,cellc,...
    :return: @order_nr: unique number ID of the purchase
    """
    LOGGER.debug('buy_aitrtime function'+str(destination))
    assert(amount!=None)
    assert(destination!=None)
    assert(network!=None)
    amount = str(amount)
    LOGGER.debug(network.strip())
    jnetwork = 'p-vodacom'
    if network.strip() == 'MTN':
        jnetwork = 'p-mtn'
    elif network.strip() == 'Vodacom':
        jnetwork = 'p-vodacom'
    elif network.strip() == 'CELLC':
        jnetwork = 'p-cellc'
    elif network.strip() == 'Eskom':
        jnetwork = 'p-eskom'
    elif network.strip() == 'Heita':
        jnetwork = 'p-heita'
    elif network.strip() == 'WorldCall':
        jnetwork = 'p-worldcall'
    elif network.strip() == 'Virgin Mobile':
        jnetwork = 'p-virginmobile'

    url = "https://ws.freepaid.co.za/airtimeplus/"
    headers = {'content-type': 'text/xml'}
    body = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:air="https://ws.freepaid.co.za/airtimeplus/">
       <soapenv:Header/>
       <soapenv:Body>
          <air:placeOrder>
             <request>
                <user>{'5883139'}</user>
                <pass>{'Free123'}</pass>
                <refno>{'5883139'}</refno>
                <network>{'{network}'}</network>
                <sellvalue>{'{amount}'}</sellvalue>
                <count>{'1'}</count>
                <extra>{'{destination}'}</extra>
             </request>
          </air:placeOrder>
       </soapenv:Body>
    </soapenv:Envelope>
    """.format(amount=amount, destination=destination, network=jnetwork)
    LOGGER.debug(body)
    try:
        response = requests.post(url, data=body, headers=headers)
    except requests.exceptions.Timeout:
        LOGGER.debug('airtime purchase: Timeout')
        response.close()
        return False
    except requests.exceptions.TooManyRedirects:
        LOGGER.debug('airtime purchase: Too many redirects')
        response.close()
        return False

    root = ET.fromstring(response.text)
    LOGGER.debug(root)
    LOGGER.debug(response.text)
    order_nr = root.find(".//orderno").text
    data = {"orderno": order_nr}
    json_data = json.dumps(data)
    LOGGER.debug(response)
    LOGGER.debug(json_data)
    #{"orderno": "2023040215205176"}
    if response.ok and data!=None:
        response.close()
        LOGGER.debug('returning order nr')
        return order_nr
    else:
        LOGGER.debug('airtime purchase: unknown error')
        response.close()
        return False


class JCronJob(CronJobBase):
    RUN_EVERY_MINS = 3 # every 2 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'incoming.my_cron_jobaofhti'    # a unique code

    def do(self):
        """check all ProcessingPurchase for activity and update db
        """
        LOGGER.debug('Jcron running..')
        LOGGER.debug('check db for uncompleted purchases')
        try:
            temp_holder = ProcessingPurchase.objects.all()
        except DatabaseError as perr:
            LOGGER.debug(perr)
        for processx in temp_holder:
            if processx.status == 'D':
                LOGGER.debug('***servicing done purchase')
                #processx.delete()
            elif processx.status == 'P':
                LOGGER.debug('servicing processing purchase')
                #check if airtime is on cellphone account
                report = report_on_airtime(order_number=processx.order_nr)
                LOGGER.debug(report)
                LOGGER.debug(type(report))
                LOGGER.debug(type(report['error_code']))
                if report['error_code'] == '000':
                    processx.status = 'D'
                    try:
                        processx.save()
                    except DatabaseError as errpr:
                        LOGGER.debug(errpr)
            elif processx.status == 'I':
                LOGGER.debug('servicing init purchase')
                try:
                    processx.status = 'P'
                    processx.save()
                except DatabaseError as derr:
                    LOGGER.debug(derr)
                # buy airtime
                # todo: raise exception and handle here for purchase error
                try:
                    LOGGER.debug('requesting airtime purchase:')
                    jorder_nr = buy_airtime(amount=processx.amount,
                                            destination=processx.number,
                                            network=processx.network
                                            )
                except Exception as exc:
                    LOGGER.debug('cannot buy airtime reliably')
                    LOGGER.debug(exc)
                LOGGER.debug('jorder_nr:'+str(jorder_nr))
                if jorder_nr:
                    processx.order_nr = jorder_nr
                else:
                    LOGGER.debug('error requesting order_number')
                try:
                    processx.save()
                except DatabaseError as derrd:
                    LOGGER.debug(derrd)
                LOGGER.debug('servicing of INIT process finished')

