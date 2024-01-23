# coding=utf-8

from django import forms

from helpers.forms.BootstrapForm import BootstrapForm
from news.models import News


class NewsForm(BootstrapForm, forms.ModelForm):

    class Meta:
        model = News
        exclude = ['published_by']
        widgets = {
            'banner_image': forms.FileInput(attrs={}),
        }
