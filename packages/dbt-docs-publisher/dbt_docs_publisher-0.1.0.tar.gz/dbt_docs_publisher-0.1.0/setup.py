"""
Setup script for dbt-docs-publisher
"""
from setuptools import setup, find_packages
import os
import re

# Read the version from __init__.py
with open(
    os.path.join(
        os.path.dirname(__file__), 
        "dbt_docs_publisher", 
        "__init__.py"
    )
) as f:
    version = re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read()
    ).group(1)

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dbt-docs-publisher",
    version=version,
    author="",
    author_email="",
    description="A CLI tool for publishing dbt docs to Azure Blob Storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dbt-docs-publisher",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "azure-storage-blob>=12.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=20.8b1",
            "flake8>=3.8.0",
            "twine>=3.4.0",
        ],
        "databricks": [
            "dbt-databricks>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ddp=dbt_docs_publisher.cli:main",
        ],
    },
) 