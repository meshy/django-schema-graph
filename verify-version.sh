#!/usr/bin/env bash

set -e

tag=$(git describe --tags --abbrev=0 --exact-match)
version=$(poetry version --short)

echo "Current git tag = ${tag}"
echo "Project version = ${version}"

if [ "${tag}" == "v${version}" ]; then
    echo "Git tag matches project version"
else
    echo "Git tag does not match project version"
    exit 1
fi

if grep "## \[${version}\]" CHANGELOG.md > /dev/null ; then
    echo "Version found in CHANGELOG.md"
else
    echo "Version not found in CHANGELOG.md"
    exit 1
fi
