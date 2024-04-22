from django.contrib import admin

from .models import Collection, Occasion, Payment


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "occasion",
        "planned_amount",
        "end_collection_date",
    )
    list_filter = ("author", "occasion", "end_collection_date")
    search_fields = ("title", "description")
    date_hierarchy = "end_collection_date"
    ordering = ("end_collection_date",)


@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "collection", "contributor", "amount", "payment_date")
    list_filter = ("collection", "contributor", "payment_date")
    search_fields = ("amount", "payment_date")
    date_hierarchy = "payment_date"
    ordering = ("payment_date",)
