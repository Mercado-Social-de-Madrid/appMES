from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from benefits.models import Benefit


# Register your models here.
@admin.register(Benefit)
class BenefitAdmin(TabbedTranslationAdmin):
    list_display = ["entity", "benefit_for_entities", "benefit_for_members", "includes_intercoop_members"]