#!/usr/bin/env python3
from setuptools import setup, find_packages
import os
import platform
import sys

# Dynamic dependencies based on platform
dependencies = [
    "boto3>=1.20.0",
    "requests>=2.25.0",
    "selenium>=4.0.0",
    "beautifulsoup4>=4.9.0",
    "configparser>=5.0.0",
]

# Platform-specific chromedriver extras
extras = {
    'windows': ['chromedriver-binary-auto'],
    'macos': ['chromedriver-binary-auto'],
    'linux': ['chromedriver-binary-auto'],
}

# Auto-detect platform for default installation
if platform.system() == 'Windows':
    dependencies.append('chromedriver-binary-auto')
elif platform.system() == 'Darwin':  # macOS
    dependencies.append('chromedriver-binary-auto')
elif platform.system() == 'Linux':
    dependencies.append('chromedriver-binary-auto')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jumpcloud-awscli",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="JumpCloud AWS CLI Authentication with Device Trust",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jumpcloud-awscli",
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