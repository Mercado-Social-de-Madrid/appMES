from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from core.models import Node, Gallery, GalleryPhoto
from core.models.social_profile import SocialNetwork, NodeSocialProfile
from django.utils.translation import gettext_lazy as _


class NodeSocialProfileInline(admin.TabularInline):
    model = NodeSocialProfile
    extra = 0
    verbose_name = _("Red Social")
    verbose_name_plural = _("Redes Sociales")


@admin.register(Node)
class NodeAdmin(TabbedTranslationAdmin):
    list_display = ["name", "shortname"]
    inlines = [NodeSocialProfileInline]


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(GalleryPhoto)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["order", "uploaded"]


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ["name", "logo"]
