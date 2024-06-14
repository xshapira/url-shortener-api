from django.contrib import admin

from shorturls.models import ShortUrl


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    ordering = ("-visits", "-created_at")
    list_display = (
        "__str__",
        "visits",
        "created_at",
        "created_time",
    )
    readonly_fields = ("created_at", "created_time")

    @admin.display(description="Created Time (ss)")
    def created_time(self, obj):
        return (
            obj.created_at.strftime("%-I:%M:%S %p")
            .replace("AM", "a.m.")
            .replace("PM", "p.m.")
        )
