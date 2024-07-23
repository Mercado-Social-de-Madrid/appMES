from modeltranslation.translator import register, TranslationOptions
from offers.models import Offer


@register(Offer)
class OfferTranslationOptions(TranslationOptions):
    fields = ('title', 'description', )
