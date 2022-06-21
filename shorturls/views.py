import json

from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import ShortUrl


class HomeView(TemplateView):
    template_name = "index.html"


@method_decorator(csrf_exempt, name="dispatch")
class ShortUrlView(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        # long_url = data.get("url")
        print(type(data))

        return "Somehing"


def redirect_to_url(request, url_key: str):
    url = get_object_or_404(ShortUrl, key=url_key)
    return redirect(url.long_url)
