from django.contrib import admin

from .models import ShortUrl


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "shorten_url",
    )
    # readonly_fields = ("shorten_url",)
