from django.contrib import admin

from .models import Version


@admin.register(Version)
class VersionInfoAdmin(admin.ModelAdmin):
    list_display = ("version", "timestamp", "git_sha", "machine_name")
    search_fields = ("version", "machine_name", "git_sha")
    date_hierarchy = "timestamp"
