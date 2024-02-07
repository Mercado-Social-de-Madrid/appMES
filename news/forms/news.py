# coding=utf-8

from django import forms
from ckeditor.widgets import CKEditorWidget

from helpers.forms.BootstrapForm import BootstrapForm
from news.models import News


class NewsForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = News
        exclude = ['published_by']
        widgets = {
            'node': forms.HiddenInput(),
            'short_description': forms.Textarea(attrs={'rows': 2}),
            'description': CKEditorWidget(attrs={'cols': 80, 'rows': 30}),
            'banner_image': forms.FileInput(attrs={}),
            'more_info_url': forms.TextInput()
        }
