from django.contrib import admin
from django.utils.translation import gettext as _

from market.models import Provider, Category, Consumer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "market", "color"]
    list_filter = ["market"]


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ["name", "member_id", "is_active", "market", ]
    list_filter = ["market", "is_active"]

@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    list_display = ["name", "member_id", "is_active", "market", ]
    list_filter = ["market", "is_active"]

    @admin.display(description=_("Nombre"))
    def name(self, obj):
        return obj.display_name
