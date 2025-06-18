from modeltranslation.translator import register, TranslationOptions

from market.models import Category, Provider
from market.models.intercoop import Intercoop


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', )

@register(Provider)
class ProviderTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description', 'services', 'legal_form')

@register(Intercoop)
class IntercoopTranslationOptions(TranslationOptions):
    fields = ('external_id_label', )
