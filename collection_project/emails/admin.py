from django.contrib import admin

from collection_project.emails.models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "to", "subject", "sent_at")
    list_filter = ("status",)
    search_fields = ("to", "subject")
    readonly_fields = ("id", "status", "to", "subject", "html", "plain_text", "sent_at", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("id", "status", "to", "subject", "html", "plain_text", "sent_at")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
    ordering = ("-created_at",)
