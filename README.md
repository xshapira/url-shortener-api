# URL Shortener

A URL shortener redirects short URLs to original (lengthy) URLs and keeps track of the number of redirects for each URL.

## TOCTOU

Concurrency is the occurrence of two or more events at the same time—two tasks overlap in execution.

TOCTOU(Time-of-Check Time-of-Use) is a type of race condition, and race condition falls under the broader category of concurrency issues. TOCTOU happens when there's a gap between the time when a condition is checked (time of check) and the time when an action is performed based on that check (time of use). In the context of our URL shortener, this can happen when multiple processes try to generate the same short URL key simultaneously.

Our program generates a random key and checks that it doesn’t already exist. Before it has a chance to write a unique shortened URL to the database, another process generates the same key and checks that it doesn’t already exist. Because tasks overlap in execution, we might wind up with a short URL that has been added with the same key after being checked but not used.

To prevent this issue, we use an atomic transaction to make sure that the key generation and database write operation are performed as a single, indivisible unit. This guarantees the uniqueness of the generated keys.

```python
@classmethod
    def generate_key(cls, long_url: str) -> ShortUrl:
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
                # If key already exists or there's database integrity violation,
                # generate a new key
                continue
```

## Incrementing the visit counter

Let's imagine multiple customers are trying to create the same key at the same time. Then we might generate the exact URL at the same time. The short URL is generated twice, but the visit counter is 1.

We can use `F expression` to update the counter (number of redirects for each URL) relative to what is in the database. The visit counter will increment by one and won't be set to a fixed value.

```python
@require_http_methods(["GET"])
def redirect_to_url(request: HttpRequest, url_key: str) -> HttpResponseRedirect:
    """
    Retrieve the ShortUrl object based on the provided key and increment its visit counter.
    Redirect the user to the original long URL.
    """
    url = get_object_or_404(ShortUrl, key=url_key)
    url.visits = F("visits") + 1
    # only `visits` field should be updated in the database
    url.save(update_fields=["visits"])
    return redirect(url.long_url)
```

## Create a new short URL

Make HTTP POST request to local API endpoint:

```bash
$ curl -X POST "http://localhost:8000/create" \
-H "Content-Type: application/json" \
-d '{"url": "https://dev.to/xshapira/using-tkinter-with-pyenv-a-simple-two-step-guide-hh5"}'


http://localhost:8000/s/djpy619
```

In this example, `http://localhost:8000/s/djpy619` will redirect to the full original URL.

## Running tests

```python
python3 manage.py test shorturls.tests
```
