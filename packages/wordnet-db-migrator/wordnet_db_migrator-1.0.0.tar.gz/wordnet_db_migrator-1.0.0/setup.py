#!/usr/bin/env python3
"""
WordNet DB Migrator - Setup Configuration

This script handles the installation of the WordNet DB Migrator package
and its dependencies.
"""
from setuptools import setup, find_packages
import sys

# Check for Python version
if sys.version_info < (3, 6):
    sys.exit("Sorry, Python < 3.6 is not supported")

setup(
    name="wordnet_db_migrator",
    version="1.0.0",
    description="A utility to migrate WordNet database from SQLite to PostgreSQL",
    url="https://github.com/onareach/wordnet_db_migrator",
    author="David Long",
    author_email="davidlong@unr.edu",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="wordnet, postgresql, sqlite, migration",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6, <4",
    install_requires=[
        "psycopg2-binary>=2.9.3",
        "pyyaml>=6.0",
        "tqdm>=4.62.0",
        "pathlib>=1.0.1;python_version<'3.4'",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.1.0",
            "flake8>=4.0.1",
            "isort>=5.9.1",
            "mypy>=0.812",
            "build>=0.7.0",
            "twine>=3.4.2",
        ],
        "data": [
            "pandas>=1.3.5",
            "numpy>=1.21.5",
        ],
        "docs": [
            "mkdocs>=1.3.0",
            "mkdocs-material>=8.2.0",
            "pymdown-extensions>=9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wordnet-db-migrator=wordnet_db_migrator.main:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/onareach/wordnet_db_migrator/issues",
        "Source": "https://github.com/onareach/wordnet_db_migrator",
    },
)
