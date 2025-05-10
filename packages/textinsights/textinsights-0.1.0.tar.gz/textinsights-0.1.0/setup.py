# Copyright (c) 2025 ksg-dev. Licensed under the MIT License. See LICENSE for details.

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="textinsights",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.4.0",
    ],
    author="ksg-dev",
    author_email="ksg.dev.data@gmail.com",
    description="A package for text analysis and visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ksg-dev/textinsights",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.6",
)