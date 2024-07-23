# -*- coding: utf-8 -*-
from ckeditor.widgets import CKEditorWidget
from django import forms

from helpers.forms.BootstrapForm import BootstrapForm
from helpers.forms.MultiLangForm import MultiLangForm
from offers.models import Offer


class OfferForm(BootstrapForm, MultiLangForm,  forms.ModelForm):

    class Meta:
        model = Offer
        exclude = []
        widgets = {
            'provider': forms.HiddenInput(),
            'description': CKEditorWidget(attrs={'cols': 80, 'rows': 30}),
            'active': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'begin_date': forms.DateInput(attrs={'type': 'hidden'}),
            'end_date': forms.DateInput(attrs={'type': 'hidden'}),
            'banner_image': forms.FileInput(attrs={}),
        }
