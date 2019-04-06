from django.apps import apps


def get_schema():
    nodes = []
    for app in apps.get_app_configs():
        for model in app.get_models():
            model_id = (app.name, model.__name__)
            nodes.append(model_id)

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
