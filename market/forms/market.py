
from django import forms
from core.models import Node
from helpers.forms.BootstrapForm import BootstrapForm


class MarketForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = Node
        widgets = {
        }
        exclude = []
