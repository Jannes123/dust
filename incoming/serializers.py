#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import DataIn, FormalCellFind, CodeFunction
import logging

LOGGER = logging.getLogger('django.request')


class DataInSerializer(serializers.Serializer):
    class Meta:
        model = DataIn
        fields = ('tag_name', 'tag_value', 'blob', 'ip_incoming')


    name = serializers.CharField(required=True)
    tag_value = serializers.CharField(required=True)
    blob = serializers.CharField(required=True)
    ip_incoming = serializers.IPAddressField(required=False)

    def create(self, validated_data):
        """
        Create and return a new `datatag` instance, given the validated data.
        """
        LOGGER.debug('serializer: datatag serializer : create : ' + str(validated_data))
        return DataIn.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `datatag` instance, given the validated data.
        """
        instance.tag_name = validated_data.get('tag_name', instance.tag_name)
        instance.tag_value = validated_data.get('tag_value', instance.tag_value)
        instance.save()
        LOGGER.debug(instance.__dict__)
        return instance

    def destroy(self, instance, validated_data):
        """
        Delete specified entry pairs.
        """
        LOGGER.debug('Serializer DataTagSerializer: delete')
        instance.tag_name = validated_data.get('tag_name', instance.tag_name)
        instance.delete()

class FormalCellFindSerializer(serializers.Serializer):
    class Meta:
       model = FormalCellFind
       fields = ('msisdn', 'phase', 'jtype', 'networkid', 'jrequest', 'jsessionid')

    msisdn = serializers.CharField(required=True)
    phase = serializers.CharField(required=True)
    jtype = serializers.IntegerField(required=True)
    networkid = serializers.IntegerField(required=True)
    jrequest = serializers.IntegerField(required=True)
    jsessionid = serializers.CharField(required=True)

    def create(self, validated_data):
        """
        Create and return a new ussd request instance, given the validated data.
        """
        LOGGER.debug('serializer: FormalCellFind serializer : create : ' + str(validated_data))
        # correct field alignment
        return FormalCellFind.objects.create(**validated_data)

    def update(self, instance, validated_data):
        LOGGER.debug('serializer:  FormalCellFind serializer : update :' + str(validated_data))
        instance.msisdn = validated_data.get('msisdn', instance.msisdn)
        instance.phase = validated_data.get('phase', instance.phase)
        instance.networkid = validated_data.get('networkid', instance.networkid)
        instance.jrequest = validated_data.get('jrequest', instance.jrequest)
        instance.jsessionid = validated_data.get('jsessionid', instance.jsessionid)
        return instance

    def destroy(self, instance, validated_data):
        """
        asdf
        """
        LOGGER.debug('serializer: FormalCellFind : destroy')
        instance.delete()


class CodeFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeFunction
        fields = ('call_log', 'network', 'amount', 'user_number', 'sponsor_number', 'timestamp', 'pay_url')

"""
    call_log = serializers.IntegerField(required=True)
    network = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)
    user_number = serializers.IntegerField(required=False)
    sponsor_number = serializers.IntegerField(required=False)
    timestamp = serializers.DateTimeField(required=True)

    def create(self, validated_data):
"""
#Create and return a new `datatag` instance, given the validated data.
"""
        LOGGER.debug('serializer: datatag serializer : create : ' + str(validated_data))
        return CodeFunction.objects.create(**validated_data)

    def update(self, instance, validated_data):
"""
#Update and return an existing `datatag` instance, given the validated data.
"""
        instance.tag_name = validated_data.get('tag_name', instance.tag_name)
        instance.tag_value = validated_data.get('tag_value', instance.tag_value)
        instance.save()
        LOGGER.debug(instance.__dict__)
        return instance

    def destroy(self, instance, validated_data):
"""
#Delete specified entry pairs.
"""
        LOGGER.debug('Serializer DataTagSerializer: delete')
        instance.tag_name = validated_data.get('tag_name', instance.tag_name)
        instance.delete()
"""

