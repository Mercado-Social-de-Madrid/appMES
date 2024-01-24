from django.contrib import admin

from core.models import Node


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ["name", "shortname"]

