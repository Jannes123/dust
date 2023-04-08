#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib import admin
from incoming.models import CodeFunction, PayInit, PayBuyer,\
    PayRequest, PayDetails, MerchantData,\
    ProductionPurchase, ProcessingPurchase


class CodeFunctionAdmin(admin.ModelAdmin):
    list_display = ('user_number', 'sponsor_number', 'timestamp')


class PayInitAdmin(admin.ModelAdmin):
    list_display = ('payeeUuid', 'payeeAccountUuid', 'payeeInvoiceNr', 'payeeOrderNr')


class PayBuyerAdmin(admin.ModelAdmin):
    list_display = ('payerName', 'payerSurname', 'payerEmail', 'payerMobile')


class PayRequestAdmin(admin.ModelAdmin):
    list_display = ('requestStatus', 'requestAmount', 'requestTokenId')


class PayDetailsAdmin(admin.ModelAdmin):
    list_display = ('paymentAmount', 'paymentDateTime', 'paymentSystemReference', 'paymentMethod')


class MerchantDataAdmin(admin.ModelAdmin):
    list_display = ('merchant_uuid', 'merchant_account_uuid', 'security_key')


class ProductionPurchaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'mobile')


class ProcessingPurchaseAdmin(admin.ModelAdmin):
    list_display = ('status', 'number', 'amount')

admin.site.register(CodeFunction, CodeFunctionAdmin)
admin.site.register(PayInit, PayInitAdmin)
admin.site.register(PayBuyer, PayBuyerAdmin)
admin.site.register(PayRequest, PayRequestAdmin)
admin.site.register(PayDetails, PayDetailsAdmin)
admin.site.register(MerchantData, MerchantDataAdmin)
admin.site.register(ProductionPurchase, ProductionPurchaseAdmin)

admin.site.register(ProcessingPurchase, ProcessingPurchaseAdmin)
