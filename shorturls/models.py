from django.db import models


class ShortUrl(models.Model):
    """ShortUrl Model Definition"""

    key = models.CharField(
        max_length=7,
        primary_key=True,
        editable=False,
        unique=True,
    )
    long_url = models.URLField(verbose_name="Long URL")
    visits = models.PositiveIntegerField(default=0, verbose_name="Visits")

    def __str__(self):
        return self.key
