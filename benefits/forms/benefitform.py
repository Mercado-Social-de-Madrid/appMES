# -*- coding: utf-8 -*-
from ckeditor.widgets import CKEditorWidget
from django import forms


from benefits.models import Benefit
from helpers.forms.BootstrapForm import BootstrapForm
from helpers.forms.MultiLangForm import MultiLangForm


class BenefitForm(BootstrapForm, MultiLangForm, forms.ModelForm):

    class Meta:
        model = Benefit
        exclude = ['published_date', 'last_updated']
        widgets = {
            'entity': forms.HiddenInput(),
            'benefit_for_entities': CKEditorWidget(attrs={'rows': 30}),
            'benefit_for_members': CKEditorWidget(attrs={'rows': 30}),
            'discount_code': forms.TextInput(attrs={'placeholder': 'Código de descuento'}),
            'discount_link_entities': forms.TextInput(attrs={ 'placeholder': 'Link del descuento para entidades'}),
            'discount_link_members': forms.TextInput(attrs={'placeholder': 'Link del descuento para socias'}),
            'discount_link_text': forms.TextInput(attrs={'placeholder': 'Texto del botón del link de descuento'}),
        }

