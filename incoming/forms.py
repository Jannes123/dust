from django import forms
from crispy_forms.layout import Fieldset, Submit, Layout, ButtonHolder
from crispy_forms.helper import FormHelper

from .models import PayInit, ProductionPurchase


class PayInitForm(forms.ModelForm):
    class Meta:
        model = PayInit
        fields = ['payeeUuid',
                  'payeeAccountUuid',
                  'payeeRefInfo',
                  'payeeCategory1',
                  'payeeCategory2',
                  'payeeCategory3',
                  'payeeSiteName',
                  'payeeSiteReference',
                  'payeeInvoiceNr',
                  'payeeOrderNr',
                  'payeeOrderItemName',
                  'payeeOrderItemName']


class ProductionPurchaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Please enter details:',
                'name',
                'surname',
                'email',
                'mobile',
                'amount'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    class Meta:
        model = ProductionPurchase
        fields = ['name', 'surname', 'email', 'mobile', 'amount']

