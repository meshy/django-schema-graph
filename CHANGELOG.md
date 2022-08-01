# Changelog for django-schema-graph

This file should be formatted as per https://keepachangelog.com/en/1.0.0/

Version numbers should follow https://semver.org/spec/v2.0.0.html


## [Unreleased]

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
