#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from django.shortcuts import reverse
import uuid

class CodeFunction(models.Model):
    """ussd integration"""
    call_log = models.IntegerField()
    network = models.CharField(max_length=32)
    amount = models.IntegerField()
    user_number = models.CharField(max_length=32)
    sponsor_number = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now=True)
    pay_url = models.CharField(default = uuid.uuid4, max_length=36)
    class Meta:
        verbose_name_plural = "incoming raw-data type custom"
        ordering = ['timestamp']

#    def __str__(self):
#        return str(self.user_number)

    def get_absolute_url(self):
        return r'/outer/{}/'.format(self.pay_url)

class PayInit(models.Model):
    """instapay info return path"""
    payeeUuid = models.CharField(max_length=36)
    payeeAccountUuid = models.CharField(max_length=36)
    payeeRefInfo = models.CharField(max_length=36)
    payeeCategory1 = models.CharField(max_length=36)
    payeeCategory2 = models.CharField(max_length=36)
    payeeCategory3 = models.CharField(max_length=36)
    payeeSiteName = models.CharField(max_length=50)
    payeeSiteReference = models.CharField(max_length=36)
    payeeInvoiceNr = models.CharField(max_length=50)
    payeeOrderNr = models.CharField(max_length=50)
    payeeOrderItemName = models.CharField(max_length=50)
    payeeOrderItemDescription = models.CharField(max_length=60)

class PayBuyer(models.Model):
    """instapay info return path"""
    payerName = models.CharField(max_length=80)
    payerSurname = models.CharField(max_length=80)
    payerEmail = models.CharField(max_length=80)
    payerMobile = models.CharField(max_length=15)


class PayRequest(models.Model):
    COMPLETED = 'C'
    EXPIRED = 'E'
    PENDING = 'P'
    CANCELLED = 'X'
    paychoices = [
            ('C', 'COMPLETED'),
            ('E', 'EXPIRED'),
            ('P', 'PENDING'),
            ('X', 'CANCELLED')
            ]
    paychoicedefault = PENDING
    requestTokenId = models.CharField(max_length=20)
    requestAmount = models.DecimalField(max_digits=5, decimal_places=2)
    requestCurrency = models.CharField(max_length=3)
    requestStatus = models.CharField(max_length=20, choices=paychoices, default=paychoicedefault)

    def get_absolute_url(self):
        return r'/pay-request/{}/'.format(self.requestTokenId)

class PayDetails(models.Model):
    detailchoices = [('D','DEPOSIT'), ('R','RECEIPT')]
    methodchoices = [('Card', 'CARD'),
            ('Card Credit', 'CARD CREDIT'),
            ('Card Debit', 'CARD DEBIT'),
            ('Cash-Wallet', 'CASH WALLET'),
            ('Default','DEFAULT'),
            ('EFT Instant', 'EFT INSTANT')
            ]
    paymentSystemReference = models.CharField(max_length=36, blank=True)
    paymentAmount = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    paymentCurrency = models.CharField(max_length=3)
    paymentDateTime = models.DateTimeField(auto_now=True)
    paymentType = models.CharField(max_length=10, choices=detailchoices)
    paymentMethod = models.CharField(max_length=12, choices=methodchoices)

class MerchantData(models.Model):
    """System setup data variables. """
    merchant_uuid = models.CharField(max_length=36)
    merchant_account_uuid = models.CharField(max_length=36)
    security_key = models.CharField(max_length=32)

class ProductionPurchase(models.Model):
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=14)

