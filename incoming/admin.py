#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib import admin
from incoming.models import DataIn, FormalCellFind, CodeFunction


class DataInAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'tag_value', 'blob', 'ip_incoming')

class FormalCellFindAdmin(admin.ModelAdmin):
    #list_display = ('msisdn', 'phase', 'jtype', 'networkid', 'jrequest', 'jsessionid', 'timestamp')
    list_display = ('msisdn', 'networkid')

class CodeFunctionAdmin(admin.ModelAdmin):
    list_display = ('user_number', 'sponsor_number', 'timestamp')

admin.site.register(DataIn, DataInAdmin)
admin.site.register(FormalCellFind, FormalCellFindAdmin)
admin.site.register(CodeFunction, CodeFunctionAdmin)
