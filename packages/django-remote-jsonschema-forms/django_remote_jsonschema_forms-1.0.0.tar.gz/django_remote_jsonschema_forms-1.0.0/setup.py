#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django_remote_jsonschema_forms",
    version="1.0.0",
    description="A platform independent form serializer for Django.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Gorka Garcia",
    author_email="ggarcia@codesyntax.com",
    url="https://github.com/codesyntax/django_remote_jsonschema_forms",
    packages=["django_remote_jsonschema_forms"],
    python_requires=">=3.9",
    install_requires=[],  # Zure benetako dependentziak hemen jartzea gomendatzen da
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
    keywords="jsonschema,react,django,python",
)

