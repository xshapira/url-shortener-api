# URL Shortener

A URL shortener redirects short URLs to original (lengthy) URLs and keeps track of the number of redirects for each
URL.

## TOCTOU

Concurrency is the occurrence of two or more events at the same time—two tasks overlap in execution. Concurrency issue referred to `TOCTOU` (Time-of-check time-of-use).

Our program generates a random key and checks that it doesn’t already exist. Before it has a chance to write a unique shortened URL to the database, another process generates the same key and checks that it doesn’t already exist. Because tasks overlap in execution, we might wind up with a short URL that has been added with the same key after being checked but not utilized.

We took care of the above by using the following logic:

```python
@classmethod
    def generate_key(cls, long_url: str):
        while True:
            key = uuid.uuid4().hex[:7]
            try:
                # We limit the outcome of a possible exception that can have
                # on any exterior transactions. We want to prevent
                # the error “current transaction is aborted,
                # queries ignored until end of transaction block”.
                with transaction.atomic():
                    return ShortUrl.objects.create(key=key, long_url=long_url)
            except IntegrityError:
                continue
```

## Incrementing the visit counter

Coming back to concurrency issues,  a common scenario could be when numerous customers are trying to create the same key at the same time. Then we might resolve the exact URL at the same time. The short URL is resolved twice, but the visit counter is 1.

We can use `F expression` to update the counter (number of redirects for each URL) relative to what is in the database. The visit counter will increment by one and won't be set to a fixed value.

```python
@require_http_methods(["GET"])
def redirect_to_url(request, url_key: str):

    """This function is called in each new short url call
    and updates the visits of that particular short url."""

    url = get_object_or_404(ShortUrl, key=url_key)
    url.visits = F("visits") + 1
    url.save(update_fields=["visits"])
    return redirect(url.long_url)
```

## Create a new short URL

Run the following API:

```bash
$ curl -X POST "http://localhost:8000/create" \
-H "Content-Type: application/json" \
-d '{"url": "https://docs.github.com/en/discussions"}'


http://localhost:8000/s/djpy619
```

In this example, <http://localhost:8000/s/djpy619> will redirect to the full [URL](https://docs.github.com/en/discussions).

## Running tests

```python
python3 manage.py test
```
