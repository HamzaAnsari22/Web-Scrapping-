from django.core.exceptions import ValidationError
from django import forms
from .models import sku_modal


class updateForm(forms.ModelForm):
    class Meta:
        model = sku_modal
        fields = '__all__'

