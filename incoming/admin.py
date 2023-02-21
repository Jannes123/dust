#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib import admin
from incoming.models import DataIn, FormalCellFind


class DataInAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'tag_value', 'blob', 'ip_incoming')

class FormalCellFindAdmin(admin.ModelAdmin):
    #list_display = ('msisdn', 'phase', 'jtype', 'networkid', 'jrequest', 'jsessionid', 'timestamp')
    list_display = ('msisdn', 'networkid')

admin.site.register(DataIn, DataInAdmin)
admin.site.register(FormalCellFind, FormalCellFindAdmin)
