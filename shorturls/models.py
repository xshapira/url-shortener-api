import uuid

from django.db import models


class ShortUrl(models.Model):

    """ShortUrl Model Definition"""

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

    # string representation of our model class instance
    def __str__(self):
        return self.key

    # overriding the default save method of parent class to customize extra fields
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    # updating the instance without modifying the key of current instance
    def update(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # generating random new key for short url
    @classmethod
    def generate_key(cls) -> str:
        while True:
            key = uuid.uuid4().hex[:7]
            if cls.objects.filter(key=key).exists():
                key = uuid.uuid4().hex[:7]
            return key

    # property representation of a short url
    @property
    def shorten_url(self):
        return f"http://localhost:8000/s/{self.key}"

    class Meta:
        verbose_name = "Short Url"
