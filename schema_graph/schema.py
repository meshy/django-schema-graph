from django.apps import apps


def get_schema():
    nodes = []
    for app in apps.get_app_configs():
        for model in app.get_models():
            nodes.append((app.name, model.__name__))

    return (
        sorted(nodes),
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    )
