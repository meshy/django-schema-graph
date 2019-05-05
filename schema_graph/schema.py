from django.apps import apps


def get_schema():
    nodes = []
    foreign_keys = []
    one_to_one = []
    many_to_many = []

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
                relationship = (model_id, related_model_id)
                if field.many_to_one:
                    foreign_keys.append(relationship)
                elif field.one_to_one and not field.auto_created:
                    one_to_one.append(relationship)
                elif field.many_to_many and not field.auto_created:
                    many_to_many.append(relationship)

    return (
        sorted(nodes),
        sorted(foreign_keys),
        sorted(one_to_one),
        sorted(many_to_many),
        [],
    )
