#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib import admin
from incoming.models import CodeFunction


class CodeFunctionAdmin(admin.ModelAdmin):
    list_display = ('user_number', 'sponsor_number', 'timestamp')

admin.site.register(CodeFunction, CodeFunctionAdmin)
