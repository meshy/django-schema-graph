# Contributing

## Building

### Javascript

The compiled JS *is not* in git.

Use `yarn` to create it:

    yarn install --frozen-lockfile
    yarn run build

For development:

    yarn install
    yarn run watch

This will watch the source files for changes and rebuild `main.js`

### Python

Create a virtualenv and install `requirements.txt`

Run `python run_test_server.py`


## Source locations
The python package is in `schema_graph` and is a Django app.

The JavaScript source is in `assets` and is compiled with `webpack` via `yarn`
