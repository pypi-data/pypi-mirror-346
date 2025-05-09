#!/usr/bin/env python3
from setuptools import setup, find_packages
import os

# Base dependencies
dependencies = [
    "boto3>=1.20.0",
    "requests>=2.25.0",
    "selenium>=4.0.0",
    "beautifulsoup4>=4.9.0",
    "configparser>=5.0.0",
]

# Optional dependencies
extras = {
    'auto-webdriver': ['webdriver-manager>=4.0.0'],
}

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jumpcloud-awscli",
    version="0.1.1",
    author="Prashant Banthia",
    author_email="prashantbanthia98@gmail.com",
    description="JumpCloud AWS CLI Authentication with Device Trust",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prashantbanthia/jumpcloud-awscli",
    packages=find_packages(),
    install_requires=dependencies,
    extras_require=extras,
    entry_points={
        "console_scripts": [
            "jumpcloud-aws=jumpcloud_aws_cli.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)