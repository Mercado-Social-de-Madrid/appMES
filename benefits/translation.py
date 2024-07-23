from modeltranslation.translator import register, TranslationOptions

from benefits.models import Benefit


@register(Benefit)
class OfferTranslationOptions(TranslationOptions):
    fields = ('benefit_for_entities', 'benefit_for_members', 'discount_link_text' )
