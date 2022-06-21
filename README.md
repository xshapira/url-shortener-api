## URL Shortener

A URL shortener redirects short URLs to original (lengthy) URLs and keeps track of the number of redirects for each
URL.

To create a new short URL run the following API:

```bash
$ curl -X POST "http://localhost:8000/create" \
-H "Content-Type: application/json" \
-d '{"url": "https://docs.github.com/en/discussions"}'


http://localhost:8000/s/djpy619
```

In this example, <http://localhost:8000/s/djpy619> will redirect to the full [URL](https://docs.github.com/en/discussions).

### Running tests

```python
python3 manage.py test
```
