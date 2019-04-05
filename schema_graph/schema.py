from django.apps import apps


def get_schema():
    nodes = []
    applications = apps.get_app_configs()
    for app in applications:
        for model in app.get_models():
            nodes.append((app.name, model.__name__))
    return sorted(nodes), []
