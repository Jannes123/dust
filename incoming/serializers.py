#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import CodeFunction, PayInit
import logging

LOGGER = logging.getLogger('django.request')


class CodeFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeFunction
        fields = ('call_log', 'network', 'amount', 'user_number', 'sponsor_number', 'timestamp', 'pay_url')


class PayInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayInit
        fields = ('payeeUuid',
                'payeeAccountUuid',
                'payeeRefInfo',
                'payeeCategory1',
                'payeeCategory2',
                'payeeCategory3',
                'payeeSiteName',
                'payeeSiteReference',
                'payeeInvoiceNr',
                'payeeOrderNr',
                'payeeOrderItemName',
                'payeeOrderItemDescription'
                )





