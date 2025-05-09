"""Setup script for the ecotracker package by everHome."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ecotracker",
    version="0.1.0",
    author="Fabian",
    author_email="user@example.com",
    description="A library for reading EcoTracker energy consumption data from everHome's local HTTP endpoint",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/ecotracker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
)