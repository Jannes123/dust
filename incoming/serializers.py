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

    def __init__(self, instance=None, data=None, **kwargs):
        LOGGER.debug("init explicit serializer")
        super(ExplicitPayInitSerializer, self).__init__(instance, data, **kwargs)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        LOGGER.debug('create')
        LOGGER.debug(validated_data)
        return PayInit.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.payeeUuid = validated_data.get('payeeUuid', instance.payeeUuid)
        instance.payeeAccountUuid = validated_data.get('payeeAccountUuid', instance.payeeAccountUuid)
        instance.payeeRefInfo = validated_data.get('payeeRefInfo', instance.payeeRefInfo)
        instance.payeeCategory1 = validated_data.get('payeeCategory1', instance.payeeCategory1)
        instance.payeeCategory2 = validated_data.get('payeeCategory2', instance.payeeCategory2)
        instance.payeeCategory3 = validated_data.get('payeeCategory3', instance.payeeCategory3)
        instance.payeeSiteName = validated_data.get('payeeSiteName', instance.payeeSiteName)
        instance.payeeSiteReference = validated_data.get('payeeSiteReference', instance.payeeSiteReference)
        instance.payeeInvoiceNr = validated_data.get('payeeInvoiceNr', instance.payeeInvoiceNr)
        instance.payeeOrderNr = validated_data.get('payeeOrderNr', instance.payeeOrderNr)
        instance.payeeOrderItemName = validated_data.get('payeeOrderItemName', instance.payeeOrderItemName)
        instance.payeeOrderItemDescription = validated_data.get('payeeOrderItemDescription', instance.payeeOrderItemDescription)
        instance.save()
        return instance
