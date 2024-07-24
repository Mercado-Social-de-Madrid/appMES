from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin

from core.models.social_profile import ProviderSocialProfile
from market.models import Provider, Category, Consumer


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ["name", "node", "color"]
    list_filter = ["node"]


class ProviderSocialProfileInline(admin.TabularInline):
    model = ProviderSocialProfile
    extra = 0
    verbose_name = _("Red Social")
    verbose_name_plural = _("Redes Sociales")


@admin.register(Provider)
class ProviderAdmin(TabbedTranslationAdmin):
    list_display = ["name", "member_id", "is_active", "node", ]
    list_filter = ["node", "is_active"]
    search_fields = ["email", "first_name", "last_name"]
    inlines = [ProviderSocialProfileInline]


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    list_display = ["name", "member_id", "is_active", "node", ]
    list_filter = ["node", "is_active"]
    search_fields = ["email", "first_name", "last_name"]

    @admin.display(description=_("Nombre"))
    def name(self, obj):
        return obj.display_name
