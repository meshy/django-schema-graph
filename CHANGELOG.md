# Changelog for django-schema-graph

This file should be formatted as per https://keepachangelog.com/en/1.0.0/

Version numbers should follow https://semver.org/spec/v2.0.0.html


## [Unreleased]


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
