from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext_lazy as _

from helpers.forms.BootstrapForm import BootstrapForm
from helpers.forms.MultiLangForm import MultiLangForm
from market.models import Provider
from market.models.intercoop import Intercoop
from django import forms

class IntercoopForm(MultiLangForm, BootstrapForm):

    class Meta:
        model = Intercoop
        widgets = {
            'node': forms.HiddenInput(),
            'description': CKEditorWidget(attrs={'cols': 190, 'rows': 5}),
        }
        exclude = ['created_at']

    def __init__(self, node, **kwargs):
        super().__init__(**kwargs)
        self.node = node
        self.fields['provider'].queryset = Provider.objects.filter(node=node)

    def clean(self):
        cleaned_data = super().clean()
        external_id_needed = cleaned_data.get('external_id_needed', False)
        if external_id_needed:
            label_filled = False
            if self.node.is_multilang_enabled:
                for lang in self.node.enabled_langs:
                    label_filled = label_filled or cleaned_data.get('external_id_label_'+lang) not in ("", None)
            else:
                label_filled = cleaned_data.get('external_id_label') not in ("", None)

            if not label_filled:
                self.add_error("external_id_label", _('Si se marca la opción para validar la socia externa, hay que introducir un valor para la etiqueta'))

        return cleaned_data