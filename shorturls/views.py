import json

from django.db.models import F
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from shorturls.models import ShortUrl


class HomeView(TemplateView):
    template_name = "index.html"


@method_decorator(csrf_exempt, name="dispatch")
class ShortUrlView(View):
    """
    View for handling the creation of short URLs.

    This class-based view is responsible for processing POST requests to create
    new short URLs. It expects a JSON payload in the request body containing the long URL to be shortened.

    The view is decorated with `@method_decorator(csrf_exempt, name="dispatch")`
    to exempt it from CSRF protection, allowing it to handle POST requests without requiring a CSRF token.

    Note:
        `csrf_exempt` is used for testing purposes only and should be removed or replaced with proper CSRF protection in a production environment.
    """

    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Create a new short URL.

        This method handles the POST request to create a new short URL.
        It expects a JSON payload in the request body.

        The method creates a new `ShortUrl` object, saves it to the database, and returns a JSON response containing the generated short URL and other details.

        Args:
            request (HttpRequest): The HTTP request object containing the JSON payload.

        Returns:
            JsonResponse: A JSON response.

            The response has a status code of 201 (created).

        Raises:
            - json.JSONDecodeError: If the JSON payload is invalid or cannot be decoded.
            - ValueError: If the "url" field is missing in the JSON payload.
        """
        try:
            data = json.loads(request.body.decode("utf-8"))
            url = ShortUrl()
            url.long_url = str(data.get("url"))
            if not url.long_url:
                raise ValueError("Missing required 'url' field in the JSON payload")
            url.save()

            current_host = url.get_current_host(request)
            url_key = url.get_absolute_url(request)
            data = {
                "success": True,
                "short_url": f"{current_host}{url_key}",
                "url": url.long_url,
            }
            return JsonResponse(data, status=201)
        except (json.JSONDecodeError, ValueError) as exc:
            return JsonResponse({"error": str(exc)}, status=400)


@require_http_methods(["GET"])
def redirect_to_url(request: HttpRequest, url_key: str) -> HttpResponseRedirect:
    """
    Redirect to the long URL associated with the provided short URL key.

    It handles the redirection from a short URL to its corresponding long URL, incrementing the visit count in the process.

    Notes:
        - The function is decorated with `@require_http_methods(["GET"])` to make sure that only GET requests are allowed.
        - The `visits` count of the ShortUrl object is incremented using the
        `F()` expression to avoid race conditions.
        - The `update_fields` parameter is used in the `save()` method to specify that only the `visits` field should be updated in the database.

    Args:
        request (HttpRequest): The HTTP request object.
        url_key (str): The unique key of the short URL.

    Returns:
        HttpResponseRedirect: A redirect response to the long URL associated with the short URL.

    Raises:
        Http404: If no ShortUrl object is found with the provided `url_key`.

    """
    url = get_object_or_404(ShortUrl, key=url_key)
    url.visits = F("visits") + 1
    url.save(update_fields=["visits"])
    return redirect(url.long_url)
