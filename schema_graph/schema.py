from django.apps import apps


def get_schema():
    nodes = []
    foreign_keys = []
    for app in apps.get_app_configs():
        for model in app.get_models():
            model_id = (app.name, model.__name__)
            nodes.append(model_id)
            for field in model._meta.get_fields():
                if not field.is_relation:
                    continue
                related_model = field.related_model
                related_app = apps.get_app_config(related_model._meta.app_label)
                related_model_id = (related_app.name, related_model.__name__)
                if field.many_to_one:
                    foreign_keys.append((model_id, related_model_id))

    return (
        sorted(nodes),
        sorted(foreign_keys),
        [],
        [],
        [],
        [],
        [],
        [],
    )
