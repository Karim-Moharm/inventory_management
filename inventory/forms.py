from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import InventoryItem


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ["name", "quantity", "sku", "unit_price", "description", "category"]

    def clean_quantity(self):
        qty = self.cleaned_data["quantity"]
        if qty > 200:
            raise forms.ValidationError("Quantity too large")
        return qty
