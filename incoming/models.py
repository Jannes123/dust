#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from django.shortcuts import reverse
import uuid


class CodeFunction(models.Model):
    """ussd integration: used for first sponsor related http request
        this entry is first saved from ussd portal then immediately returned
        by rest framework as xml response.
    """
    call_log = models.IntegerField()
    network = models.CharField(max_length=32)
    amount = models.IntegerField()
    user_number = models.CharField(max_length=32)
    sponsor_number = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now=True)
    pay_url = models.CharField(default=uuid.uuid4, max_length=36)

    class Meta:
        verbose_name_plural = "incoming raw-data type custom"
        ordering = ['timestamp']

#    def __str__(self):
#        return str(self.user_number)

    def get_absolute_url(self):
        return r'/outer/{}/'.format(self.pay_url)


class ProductionPurchase(models.Model):
    """
    Second phase data is captured from second user via http form.
    """
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=14)
    # todo: add network attr like above
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    original_url_unique = models.ForeignKey(
        'CodeFunction',
        on_delete=models.CASCADE,
        null=True, blank=True
    )


class PayInit(models.Model):
    """instapay info return path
    Notification from notify url populates this table's entries.
    payeeRefInfo must be equal to ‘m_tx_order_nr’ from request.
    """
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
    """Should be completed upon notification return from instapay.
        A pending request means ptmu is waiting on another system for updates.
    """
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
    requestTokenId = models.CharField(max_length=20, blank=True)
    requestAmount = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    requestCurrency = models.CharField(max_length=3, default='ZAR', blank=True)
    requestStatus = models.CharField(max_length=1, choices=paychoices, default=paychoicedefault, blank=False)
    init = models.ForeignKey(
        'PayInit',
        on_delete=models.CASCADE,
        null=True, blank=True
    )# payeeRefInfo must be equal to ‘m_tx_order_nr’ from request.

    def get_absolute_url(self):
        return r'/pay-request/{}/'.format(self.requestTokenId)


class PayDetails(models.Model):
    """additional info on transaction used for uniquely id of transactions"""
    detailchoices = [('D', 'DEPOSIT'), ('R', 'RECEIPT')]
    methodchoices = [('Card', 'CARD'),
                     ('Card Credit', 'CARD CREDIT'),
                     ('Card Debit', 'CARD DEBIT'),
                     ('Cash-Wallet', 'CASH WALLET'),
                     ('Default', 'DEFAULT'),
                     ('EFT Instant', 'EFT INSTANT')
                     ]
    paymentSystemReference = models.CharField(max_length=36, blank=True)
    paymentAmount = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    paymentCurrency = models.CharField(max_length=3)
    paymentDateTime = models.DateTimeField(auto_now=True)
    paymentType = models.CharField(max_length=10, choices=detailchoices)
    paymentMethod = models.CharField(max_length=12, choices=methodchoices)
    init = models.ForeignKey(
        'PayInit',
        on_delete=models.CASCADE,
        null=True, blank=True
    )


class MerchantData(models.Model):
    """System setup data variables. """
    merchant_uuid = models.CharField(max_length=36)
    merchant_account_uuid = models.CharField(max_length=36)
    security_key = models.CharField(max_length=32)
    merchant_shortcode = models.CharField(max_length=36, null=True, blank=True)#merchant shortcode allocated by trustlink
    current_invoice_number = models.IntegerField()


