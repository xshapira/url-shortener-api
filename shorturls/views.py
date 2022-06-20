from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

# from .models import ShortUrl


class HomeView(TemplateView):
    template_name = "index.html"

@csrf_exempt
def short_url(request):
