import logging

from django.conf import settings
from pydeps import cli, py2depgraph, target

from .schema import Schema

log = logging.getLogger(__name__)


def _get_label(name):
    return _split_name(name)[0]


def _split_name(name):
    result = name.split('.', 1)
    if len(result) == 1:
        return [result[0]] * 2
    return result


def get_modules_as_schema(base_dir):
    cli.verbose = lambda *args: log.debug(*args)
    MAX_BACON = 2  # default: 2**65
    EXCLUDE_MODULES = [
        'django'
    ]

    excludes = []
    for name in EXCLUDE_MODULES:
        # excludes.append(name)
        excludes.append(name+'.*')
    kwargs = dict(
        T='svg', config=None, debug=False, display=None, exclude=excludes,
        exclude_exact=[],
        externals=False, format='svg', max_bacon=MAX_BACON, no_config=True,
        nodot=False,
        noise_level=2**65, noshow=True, output=None, pylib=False, pylib_all=False,
        show=False, show_cycles=False, show_deps=False, show_dot=False,
        show_raw_deps=False, verbose=0, include_missing=True, start_color=0
    )
    graph = py2depgraph.py2dep(target.Target(base_dir), **kwargs)

    nodes = set()
    imports = set()
    for a, b in graph:
        # b imports a
        nodes.add(a.name)
        nodes.add(b.name)
        new_import = [tuple(_split_name(b.name)), tuple(_split_name(a.name))]
        log.debug("adding import %s", new_import)
        imports.add(tuple(new_import))

    models = {}
    for name in nodes:
        label, short_name = _split_name(name)
        models.setdefault(label, set()).add(short_name)

    for app_group in models.keys():
        models[app_group] = sorted(models[app_group])

    return Schema(
        # Vertices
        abstract_models={},
        models=models,
        proxies=[],
        # Edges
        foreign_keys=sorted(imports),
        inheritance=[],
        many_to_manys=[],
        one_to_ones=[],
    )

