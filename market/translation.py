from modeltranslation.translator import register, TranslationOptions

from market.models import Category, Provider


@register(Category)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', )

@register(Provider)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description', 'legal_form')