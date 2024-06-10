import uuid

from django.db import IntegrityError, models, transaction


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

    @classmethod
    def generate_key(cls, long_url: str):
        """
        Generate a unique key and create a ShortUrl object with the given long URL.

        Args:
            long_url (str): The long URL for which a short URL key will be generated.

        Returns:
            ShortUrl: The ShortUrl object created with the generated key and provided long URL.

        Raises:
            IntegrityError: If a ShortUrl object with the generated key already exists, a new key will be generated.
        """

        while True:
            key = uuid.uuid4().hex[:7]
            try:
                # We limit the outcome of a possible exception that can have
                # on any exterior transactions. We want to prevent the error:
                # "current transaction is aborted, queries ignored until end of
                # transaction block".
                with transaction.atomic():
                    return ShortUrl.objects.create(key=key, long_url=long_url)
            except IntegrityError:
                continue
