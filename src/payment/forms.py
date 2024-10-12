from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    shipping_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}), required=True)
    shipping_email =  forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Email'}), required=True)
    shipping_phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Phone Number'}), required=True)
    shipping_address =  forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Address'}), required=True)
    shipping_city =  forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping City'}), required=True)
    shipping_state =  forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping State'}), required=False)
    shipping_country =  forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Country'}), required=False)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_name', 'shipping_email', 'shipping_phone', 'shipping_address', 'shipping_city', 'shipping_state', 'shipping_country']

        exclude = ['user', ]