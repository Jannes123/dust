from django import forms

from .models import PayInit

class PayInitForm(forms.ModelForm):
    class Meta:
        model = PayInit
        fields = ['payeeUuid', 'payeeAccountUuid', 'payeeRefInfo', 'payeeCategory1', 'payeeCategory2', 'payeeCategory3', 'payeeSiteName', 'payeeSiteReference', 'payeeInvoiceNr', 'payeeOrderNr', 'payeeOrderItemName', 'payeeOrderItemName']


class ProductionPurchaseForm():
    class Meta:
        model = ProductionPurchase
        fields = ['name', 'surname', 'email', 'mobile']
