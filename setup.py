#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup configuration for HTTP Request Builder.
"""

from setuptools import setup, find_packages
import os
import sys

# Leer el README para la descripción larga
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Leer requirements
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="http-request-builder",
    version="0.1.0",
    author="Falconmx1",
    author_email="tu-email@ejemplo.com",
    description="Herramienta CLI para probar, depurar y monitorear APIs REST",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Falconmx1/http-request-builder",
    project_urls={
        "Bug Tracker": "https://github.com/Falconmx1/http-request-builder/issues",
        "Documentation": "https://github.com/Falconmx1/http-request-builder/wiki",
        "Source Code": "https://github.com/Falconmx1/http-request-builder",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
        ],
    },
    entry_points={
        'console_scripts': [
            'http-request-builder=main:main',
            'hrb=main:main',  # Alias corto
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
