from django.contrib import admin

from news.models import News


# Register your models here.
@admin.register(News)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ["title", "node", ]
    list_filter = ["node"]