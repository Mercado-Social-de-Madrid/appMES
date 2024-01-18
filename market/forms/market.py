
from django import forms
from core.models import Market
from helpers.forms.BootstrapForm import BootstrapForm


class MarketForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = Market
        widgets = {
        }
        exclude = []
