import os
import sys

from setuptools import Command, find_packages, setup


version = "1.1.0"


with open("README.md", "r") as fh:
    long_description = fh.read()


class VerifyVersionCommand(Command):
    """Custom command to verify that the git tag matches our version."""

    description = "verify that the git tag matches our version"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tag = os.getenv("GITHUB_REF")

        if tag == "refs/tags/v" + version:
            print("Git tag: {0} matches expected version.".format(tag))
        else:
            info = "Git tag: {0} does not match the version of this app: v{1}".format(
                tag, version
            )
            sys.exit(info)


setup(
    author="Charlie Denton",
    author_email="charlie@meshy.co.uk",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Database",
        "Topic :: Documentation",
        "Topic :: Utilities",
    ],
    cmdclass={"verify": VerifyVersionCommand},
    description="An interactive graph of your Django model structure.",
    include_package_data=True,
    install_requires=["attrs"],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="django-schema-graph",
    packages=find_packages(exclude=["tests", "tests.*"]),
    url="https://github.com/meshy/django-schema-graph",
    version=version,
)
