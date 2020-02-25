from schema_graph.views import Schema


try:
    # Django 2+:
    from django.urls import path

    urlpatterns = [path("", Schema.as_view())]
except ImportError:
    # Django < 2:
    from django.conf.urls import url

    urlpatterns = [url(r"^$", Schema.as_view())]
