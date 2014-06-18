#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='Adamo Calibrator',
    version='0.0.1',
    author='Nicolás Illia',
    author_email='nillia@msa.com.ar',
    packages=['adamo_calibrator'],
    include_package_data=True,
    package_data={
        'adamo_calibrator/ui/web/html': ['*'],
    },
    scripts=[],
    url='http://pypi.python.org/pypi/---/',
    license='LICENSE.txt',
    description='A Python touchscreen calibrator.',
    long_description=open('README.txt').read(),
    install_requires=["zaguan"],
)
