#!/usr/bin/env bash

set -e

tag=${GITHUB_REF}
version=$(poetry version --short)

echo "GITHUB_REF = ${tag}"
echo "Project version = ${version}"

if [ "${tag}" == "${version}" ]; then
    echo "GitHub ref matches project version."
else
    echo "GitHub ref does not match project version."
    exit 1
fi
