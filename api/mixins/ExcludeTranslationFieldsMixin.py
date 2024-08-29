from modeltranslation.fields import TranslationField


class ExcludeTranslationFieldsMixin:
    # Exclude the specific language fields from the serializer output

    def get_fields(self):
        fields = super().get_fields()
        for f in self.Meta.model._meta.fields:
            if f.name in fields and isinstance(f, TranslationField):
                del fields[f.name]
        return fields
