from setuptools import setup, find_packages


def parse_requirements(filename):
    """load requirements from a pip requirements file"""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


setup(
    name="lightquant",
    version="0.1.1",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    author="Pankaj Sharma",
    description="A lightweight Python library for python utilities for holidays, dates, options and other tools",
    url="https://bitbucket.org/incurrency/lightquant",
    license="MIT",
)
