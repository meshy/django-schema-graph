# Changelog for django-schema-graph

This file should be formatted as per https://keepachangelog.com/en/1.0.0/

Version numbers should follow https://semver.org/spec/v2.0.0.html


## [Unreleased]

### Added

- Hovering over a node now shows a tooltip with its name, group, and tags.

## [3.0.0] - 2023-05-14

### Backwards incompatible

- Dropped support for Django < 3.2.
- Dropped support for Python < 3.10.
- Data format returned from `schema_graph.schema.get_schema` has been overhauled.
- Template context now only includes the new schema data format.
- The JS front-end has been rewritten to handle the new format.


### Changed

- Main "App" Vue component refactored into smaller component files.
- The JS code now tries to refer to "nodes" and "edges", not "models" and "apps".
- More options have been added to the sidebar to offer finer control.
  This has resulted in the sidebar getting wider.
- The list of groups in the sidebar is now collapsed by default.
- More items in the sidebar show tooltips on hover (using the title HTML attribute).
- Graph nodes representing Proxy models now appear with a white background.


## [2.2.1] - 2022-10-26

## Fixed

- Use `>=` to define minimum version numbers, not `~X.Y.Z`.
  This fixes an issue where installing alongside other versions of `attrs`
  caused an error:
  `django-schema-graph 2.2.0 depends on attrs<22.0.0 and >=21.4.0`


## [2.2.0] - 2022-10-26

### Added

- Added Python 3.11 support.
- Added Django 4.1 support.

### Changed

- Remove upper boundary on supported Python version.
- Python 3.10 tests now only run against Django 3.2+, because Django <3.2 does
  not support Python 3.10.
- Specify a minimum `attrs` version of `21.4.0`.

## Fixed

- Fix broken CI by removing `tox-poetry-dev-dependencies`.


## [2.1.0] - 2022-08-01

### Added

- Introduced `SCHEMA_GRAPH_VISIBLE` setting as a way to control access to the
  `Schema` view. We will continue to default to using `DEBUG`.


### Changed

- We no longer use a decorator on the `Schema` view to override `dispatch`, and
  now override it directly.
- It is now possible to control access to the `Schema` view by subclassing and
  overriding the `access_permitted` function.


## [2.0.0] - 2022-08-01

### Backwards incompatible

- Dropped Python 2 support.
- Dropped Python 3.5 support.
- Dropped Django 1.8 support. 1.11 is now the minimum supported version.

### Added

- Added Python 3.9 support.
- Added Python 3.10 support.
- Added Django 3.1 support.
- Added Django 3.2 support.
- Added Django 4.0 support.

### Changed

- Moved from `setup.py` to `poetry` for building released packages.

### Fixed

- Many-to-many connections aren't added when using explicit through models.
  The foreign-key connections from the through table are enough. #46


## [1.2.0] - 2020-03-01

### Added

- Collapsed model groups (apps) are now visible on the graph.
- Expand-all / Collapse-all buttons in sidebar.
- Show-all / Hide-all buttons in sidebar.


## [1.1.0] - 2020-02-26

### Added

- Abstract base models are now visible.
- Proxy models now clearly show what they proxy.
- Inheritance is visible as a new kind of connection.

## [1.0.0] - 2020-02-23

### Added

- Ability to dynamically change the apps and models being displayed via a new
  sidebar.
- Colours. So many pretty colours.

## [0.0.2] - 2020-02-20

### Changed
- Hopefully nothing other than version number. This tests automatic releases to
  PyPI with GitHub actions.

## [0.0.1] - 2020-02-19

### Added
- Basic schema graph. Interactive, but no dynamic data yet. Tested with Django
  1.8, and 1.11-3.0 on Python 2.7 and 3.5+ (where those combinations make sense).
