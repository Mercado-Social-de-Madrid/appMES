# coding=utf-8

from django import forms
from modeltranslation.fields import TranslationField

# Mixin form to apply the same widget to translation fields than its base field (for multi-lang forms)
class MultiLangForm(forms.ModelForm):

    def __init__(self, *args, ** kwargs):
        super().__init__(*args, **kwargs)
        for f in self._meta.model._meta.fields:
            if f.name in self.fields and isinstance(f, TranslationField):
                self.fields[f.name].widget = self.fields[f.translated_field.name].widget
