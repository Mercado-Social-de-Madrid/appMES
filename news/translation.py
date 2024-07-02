from modeltranslation.translator import register, TranslationOptions
from news.models import News

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'description', 'more_info_text')
