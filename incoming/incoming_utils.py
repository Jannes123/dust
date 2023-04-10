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
    LOGGER.debug('order_status:')
    data = {"error_code": error_code}

    json_data = json.dumps(data)
    return data


def buy_airtime(amount, destination, network, process):
    LOGGER.debug('buy_aitrtime function'+str(destination))
    assert(amount!=None)
    assert(destination!=None)
    assert(network!=None)
    amount = str(amount)
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
    """.format(amount=amount, destination=destination, network='p-vodacom')
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
    process.order_number = order_nr
    data = {"orderno": order_nr}
    json_data = json.dumps(data)
    LOGGER.debug(response)
    LOGGER.debug(json_data)
    #{"orderno": "2023040215205176"}
    if response.ok and data!=None:
        response.close()
        LOGGER.debug('returning order nr')
        return data
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
                #todo: if success move to done
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
                                            number=processx.number,
                                            network=processx.network
                                            )
                except ConnectionError as exc:
                    LOGGER.debug('cannot buy airtime reliably')
                LOGGER.debug('jorder_nr:'+str(jorder_nr))
                processx.order_nr = jorder_nr
                try:
                    processx.save()
                except DatabaseError as derrd:
                    LOGGER.debug(derrd)
                LOGGER.debug('servicing of INIT process finished')

