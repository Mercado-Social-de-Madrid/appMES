from django.contrib import admin

from modeltranslation.admin import TabbedTranslationAdmin
from news.models import News



@admin.register(News)
class NewsAdmin(TabbedTranslationAdmin):
    list_display = ["title", "node", ]
    list_filter = ["node"]