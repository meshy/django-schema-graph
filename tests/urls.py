import os

from schema_graph.views import Modules, Schema


base_dir = os.path.dirname(__file__)

try:
    # Django 2+:
    from django.urls import path

    urlpatterns = [
        path("", Schema.as_view()),
        path("deps", Schema.as_view()),
    ]
except ImportError:
    # Django < 2:
    from django.conf.urls import url

    urlpatterns = [
        url(r"^$", Schema.as_view()),
        url(r"^deps$", Modules.as_view(base_dir=base_dir)),
    ]
