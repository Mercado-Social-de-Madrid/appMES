from django.contrib import admin

from core.models import Market
from django.contrib.auth.urls import *

# Register your models here.

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ["name", "shortname"]

