from modeltranslation.fields import TranslationField


class ExcludeTranslationFieldsMixin:
    # Exclude the specific language fields from the serializer output

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        for f in self.Meta.model._meta.fields:
            if f.name in self.fields and isinstance(f, TranslationField):
                self.fields.pop(f.name)