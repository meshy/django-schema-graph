from django.contrib import admin
from schema_graph.views import Schema


try:
    # Django 2+:
    from django.urls import path, include

    urlpatterns = [
        path('admin/doc/', include('django.contrib.admindocs.urls')),
        path('admin/', admin.site.urls),
        path("", Schema.as_view())
    ]
except ImportError:
    # Django < 2:
    from django.conf.urls import url

    urlpatterns = [
        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
        url('^admin/', admin.site.urls),
        url(r"^$", Schema.as_view())
    ]
