#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#__doc__ = """supporting functions for incoming app"""

from django_cron import CronJobBase, Schedule
import requests
import xml.etree.ElementTree as ET
import json
import sys

import logging
LOGGER = logging.getLogger('django.request')
LOGGER.debug(sys.path)


class JCronJob(CronJobBase):
    RUN_EVERY_MINS = 3 # every 2 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'incoming.my_cron_jobaofhti'    # a unique code

    def do(self):
        """check all ProcessingPurchase for activity and update db
        """
        LOGGER.debug('Jcron running..')
        LOGGER.debug('check db for uncompleted purchases')


def buy_airtime(amount, destination):
    LOGGER.debug('buy_aitrtime:')
    assert(amount!=None)
    assert(destination!=None)
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
                <network>{'p-vodacom'}</network>
                <sellvalue>{'{amount}'}</sellvalue>
                <count>{'1'}</count>
                <extra>{'{destination}'}</extra>
             </request>
          </air:placeOrder>
       </soapenv:Body>
    </soapenv:Envelope>
    """.format(amount=amount, destination=destination)
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
    order_nr = root.find(".//orderno").text
    data = {"orderno": order_nr}
    json_data = json.dumps(data)
    LOGGER.debug(response)
    LOGGER.debug(json_data)
    #{"orderno": "2023040215205176"}
    if response.ok and data!=None:
        response.close()
        return True
    else:
        LOGGER.debug('airtime purchase: unknown error')
        response.close()
        return False
