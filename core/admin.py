from django.contrib import admin

from core.models import Node, Gallery, GalleryPhoto


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ["name", "shortname"]

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["title"]

@admin.register(GalleryPhoto)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["order", "uploaded"]
