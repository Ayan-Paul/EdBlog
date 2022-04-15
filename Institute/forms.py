from django import forms
from .models import Institute

class InstituteForm(forms.ModelForm):
    class Meta:
        model = Institute
        fields = ('name',)

