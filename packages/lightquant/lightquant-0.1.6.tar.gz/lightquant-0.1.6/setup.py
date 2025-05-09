import os
from setuptools import setup, find_packages


def parse_requirements(filename):
    """load requirements from a pip requirements file"""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "lightquant", "__init__.py")
    with open(version_file, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name="lightquant",
    version=get_version(),  # Dynamically get version from __init__.py
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    author="Pankaj Sharma",
    description="A lightweight Python library for python utilities for holidays, dates, options and other tools",
    url="https://bitbucket.org/incurrency/lightquant",
    license="MIT",
)
