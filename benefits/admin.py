from django.contrib import admin

from benefits.models import Benefit


# Register your models here.
@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ["entity", "benefit_for_entities", "benefit_for_members", "includes_intercoop_members"]