#!/usr/bin/env bash

set -e

tag=${GITHUB_REF}
version=$(poetry version --short)

echo "GITHUB_REF = ${tag}"
echo "Project version = ${version}"

if [ "${tag}" == "v${version}" ]; then
    echo "GitHub ref matches project version."
else
    echo "GitHub ref does not match project version."
    exit 1
fi

if grep "## \[${version}\]" CHANGELOG.md > /dev/null ; then
    echo "Version found in CHANGELOG.md"
else
    echo "Version not found in CHANGELOG.md"
    exit 1
fi
