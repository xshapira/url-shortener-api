from django.contrib import admin

from shorturls.models import ShortUrl


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    ordering = ("-visits",)
    list_display = ("__str__", "visits", "created_at")
    readonly_fields = ("created_at",)
