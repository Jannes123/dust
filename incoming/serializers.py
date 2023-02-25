#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import CodeFunction
import logging

LOGGER = logging.getLogger('django.request')

class CodeFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeFunction
        fields = ('call_log', 'network', 'amount', 'user_number', 'sponsor_number', 'timestamp', 'pay_url')

