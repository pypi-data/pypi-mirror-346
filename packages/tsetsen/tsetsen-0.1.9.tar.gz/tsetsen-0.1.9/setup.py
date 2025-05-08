#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import re

# Read version from package without importing
with open(os.path.join("src", "tsetsen", "__init__.py"), "r") as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    version = version_match.group(1) if version_match else "0.1.0"

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Required packages
REQUIRED = [
    "grpcio>=1.40.0",
    "protobuf>=3.19.0",
]

# Optional packages
EXTRAS = {
    "dev": [
        "pytest>=6.0.0",
        "black>=21.5b2",
        "mypy>=0.812",
        "grpcio-tools>=1.40.0",
        "twine>=3.4.1",
    ],
}

# Setup configuration
setup(
    name="tsetsen",
    version=version,
    description="Python SDK for the Tsetsen, Mongolian Text-to-Speech API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tsetsen AI",
    author_email="info@tsetsen.ai",
    python_requires=">=3.10",
    url="",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    keywords=["tts", "text-to-speech", "api", "grpc", "speech synthesis"],
    project_urls={},
)
