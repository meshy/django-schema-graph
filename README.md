# Django Schema Graph

## Installation

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'schema_graph',
    ...
]
```

Add to your URLs.

```python
from schema_graph.views import Schema
urlpatterns += [
    path("schema/" Schema.as_view()),
]
```

Or, on Django < 2:

```python
urlpatterns += [
    url(r"^schema/$", Schema.as_view()),
]
```


# Use

Browse to `/schema/` (assuming that's where you put it in your URLs).

Note: `DEBUG` mode is required, on the assumption that you don't want to leak
sensitive information about your website outside of local development.
