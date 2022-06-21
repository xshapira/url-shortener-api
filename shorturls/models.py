import uuid

from django.db import models


class ShortUrl(models.Model):

    """ """

    key = models.CharField(
        max_length=7,
        primary_key=True,
        editable=False,
    )
    long_url = models.URLField(verbose_name="Long URL")
    visits = models.PositiveIntegerField(default=0, verbose_name="Visits")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls) -> str:
        key = uuid.uuid4().hex[:7]
        count = 0
        while cls.objects.filter(key=key).exists() or count > 7:
            key = uuid.uuid4().hex[:7]
            count += 1
        return key

    @property
    def shorten_url(self):
        return f"http://localhost:8000/s/{self.key}"

    class Meta:
        verbose_name = "link"
        verbose_name_plural = "Most viewed links"
