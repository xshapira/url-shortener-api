from django.urls import path

from shorturls.views import ShortUrlView, redirect_to_url

urlpatterns = [
    path("create", ShortUrlView.as_view(), name="create"),
    path("s/<url_key>", redirect_to_url, name="entry_point"),
]
