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


class ExplicitPayInitSerializer(serializers.Serializer):
    payeeUuid = serializers.CharField(max_length=36)
    payeeAccountUuid = serializers.CharField(max_length=36)
    payeeRefInfo = serializers.CharField(max_length=36)
    payeeCategory1 = serializers.CharField(max_length=36)
    payeeCategory2 = serializers.CharField(max_length=36)
    payeeCategory3 = serializers.CharField(max_length=36)
    payeeSiteName = serializers.CharField(max_length=50)
    payeeSiteReference = serializers.CharField(max_length=36)
    payeeInvoiceNr = serializers.CharField(max_length=50)
    payeeOrderNr = serializers.CharField(max_length=50)
    payeeOrderItemName = serializers.CharField(max_length=50)
    payeeOrderItemDescription = serializers.CharField(max_length=60)

    def __init__(self):
        LOGGER.debug("init explicit serializer")
        super(ExplicitPayInitSerializer, self).__init__()

