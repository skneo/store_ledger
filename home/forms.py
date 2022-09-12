# import form class from django
from django import forms

# import GeeksModel from models.py
from .models import Transactions

# create a ModelForm


class TransactionsForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Transactions
        fields = "__all__"
        exclude = ('material_code', 'material_name', 'inv_id', 'balance',)
    CHOICES = [('OUT', 'OUT'), ('IN', 'IN')]
    in_out = forms.ChoiceField(choices=CHOICES)

    def __init__(self, *args, **kwargs):
        super(TransactionsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2'
