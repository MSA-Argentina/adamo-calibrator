#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='adamo_calibrator',
    version='0.2.0',
    author='Nicolas Illia',
    author_email='nillia@msa.com.ar',
    packages=['adamo_calibrator'],
    include_package_data=True,
    scripts=[],
    url='https://pypi.python.org/pypi/adamo_calibrator',
    license='LICENSE.txt',
    description='A touchscreen calibrator.',
    long_description=open('README.txt').read(),
    install_requires=["zaguan"],
    entry_points={
        'console_scripts': ['adamo-calibrator = adamo_calibrator:run']
    },
)
