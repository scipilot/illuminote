# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='illuminote',
    version='0.1.0',
    description='Illuminote - guitar fretboard visual tutor',
    long_description=readme,
    author='Pip Jones',
    author_email='code@scipilot.org',
    url='https://github.com/scipilot/illumunote',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)


# TODO: Also see https://github.com/pypa/sampleproject/blob/master/setup.py

