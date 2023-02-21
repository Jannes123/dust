#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.apps import AppConfig

class IncomingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'incoming'
    verbose_name = "send incoming ussd request structured-info to database"

