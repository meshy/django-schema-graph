from django.urls import path

from schema_graph.views import Schema


urlpatterns = [path("", Schema.as_view())]
