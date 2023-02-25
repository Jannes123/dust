#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from django.shortcuts import reverse
import uuid

class CodeFunction(models.Model):
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

    def __str__(self):
        return str(self.user_number)

    def get_absolute_url(self):
        return r'/outer/{}/'.format(self.pay_url)

