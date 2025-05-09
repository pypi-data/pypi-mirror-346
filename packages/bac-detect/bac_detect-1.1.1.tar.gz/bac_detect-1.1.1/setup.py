#!/usr/bin/env python3
"""
A simple setup.py for backward compatibility with older tools.
The package metadata is in pyproject.toml.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bac_detect",
    version="1.1.1",
    author="Ruslan",
    description="Detect backdoors in Python, JS and PHP code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WaiperOK/bac_detect",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={"bac_detect": ["patterns.json"]},
    entry_points={
        "console_scripts": [
            "bac_detect=bac_detect.backdoor_detector:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "bandit>=1.7.0",
        "pylint>=2.13.0",
        "esprima>=4.0.1",
        "tqdm>=4.0.0",
    ],
) 