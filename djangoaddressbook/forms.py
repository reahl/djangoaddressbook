from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('name', 'email_address', '_version')
        widgets = {'_version': forms.HiddenInput()}
