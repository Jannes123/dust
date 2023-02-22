#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from django.shortcuts import reverse
import uuid

class DataIn(models.Model):
    tag_name = models.CharField(max_length=255)
    tag_value = models.CharField(max_length=255)
    blob = models.CharField(max_length=800)
    ip_incoming = models.GenericIPAddressField()

class FormalCellFind(models.Model):
    msisdn = models.CharField(max_length=255)
    phase =  models.CharField(max_length=255)
    jtype = models.IntegerField()
    networkid = models.IntegerField()
    jrequest = models.IntegerField()
    jsessionid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "incoming raw-data type 1"

    def __str__(self):
        return str(self.msisdn)

class CodeFunction(models.Model):
    call_log = models.IntegerField()
    network = models.CharField(max_length=32)
    amount = models.IntegerField()
    user_number = models.IntegerField()
    sponsor_number = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    pay_url = models.CharField(default = uuid.uuid4, max_length=36)
    class Meta:
        verbose_name_plural = "incoming raw-data type custom"
        ordering = ['timestamp']

    def __str__(self):
        return str(self.user_number)

    def get_absolute_url(self):
        return r'/outer/{}/'.format(self.pay_url)


