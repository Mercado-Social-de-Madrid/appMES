# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.
from offers.models import Offer


@admin.register(Offer)
class OffersAdmin(admin.ModelAdmin):

    def pub_date(self, obj):
        return obj.published_date.strftime("%d/%m/%Y")

    def begin_date_format(self, obj):
        return obj.begin_date.strftime("%d/%m/%Y") if obj.begin_date else ''

    def end_date_format(self, obj):
        return obj.end_date.strftime("%d/%m/%Y") if obj.end_date else ''

    def provider_name(self, obj):
        return obj.provider.display_name

    list_display = ('provider_name', 'title', 'active', 'pub_date', 'begin_date_format', 'end_date_format')
    ordering = '-published_date',
    pub_date.short_description = 'Publicado'
    begin_date_format.short_description = 'Fecha inicio'
    end_date_format.short_description = 'Fecha fin'
