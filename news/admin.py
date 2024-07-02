from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from news.models import News


# Register your models here.
@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ["title", "node", ]
    list_filter = ["node"]