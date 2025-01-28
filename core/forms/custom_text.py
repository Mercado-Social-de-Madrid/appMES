import logging

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _
from modeltranslation.fields import TranslationField

from core.models import Node
from core.models.custom_text import CustomizableText, NodeCustomText, CustomizableTextContext
from core.models.social_profile import SocialNetwork, ProviderSocialProfile, SocialProfile, NodeSocialProfile
from helpers.forms.BootstrapForm import BootstrapForm
from helpers.forms.MultiLangForm import MultiLangForm
from helpers.widgets.SocialNetworkWidget import SocialNetworkWidget

logger = logging.getLogger(__name__)


class NodeCustomTextForm(BootstrapForm, MultiLangForm, forms.ModelForm):
    string = forms.CharField(required=False)

    class Meta:
        model = NodeCustomText
        exclude = []
        widgets = {
            'node': forms.widgets.HiddenInput(),
            'text_id': forms.widgets.HiddenInput(),
            'string': forms.widgets.Textarea()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'initial' in kwargs:
            text_id = kwargs.get('initial').get('text_id')
            if not 'title' in text_id.id:
                for key in self.fields:
                    if 'string' in key:
                        self.fields[key].widget = CKEditorWidget(attrs={'required':False, 'cols': 80, 'rows': 30})

        
    @staticmethod
    def get_initial(node, initial_texts=None):
        customizable_texts = CustomizableText.objects.all()
        texts_data = []
        for text in customizable_texts:
            string = None
            text_values = {
                'node': node,
                'text_id': text,
                'string': string
            }
            if initial_texts and initial_texts.filter(text_id=text).exists():
                custom_text = initial_texts.get(text_id=text)
                for f in getattr(NodeCustomText, '_meta').model._meta.fields:
                    if isinstance(f, TranslationField):
                        text_values[f.name] = getattr(custom_text, f.name)

            texts_data.append(text_values)
        return texts_data

    @staticmethod
    def getNodeCustomTextsFormset():
        formset = formset_factory(form=NodeCustomTextForm, extra=0)
        return formset
