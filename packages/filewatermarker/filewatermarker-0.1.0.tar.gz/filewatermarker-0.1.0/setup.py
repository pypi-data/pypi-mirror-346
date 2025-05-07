"""
Setup script for backward compatibility with pip.

This file exists for backward compatibility with tools that don't support
pyproject.toml. The main package configuration is in pyproject.toml.
"""

from setuptools import setup

if __name__ == "__main__":
    setup()
