#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'numpy',
    'pandas',
    'pillow',
    'tensorflow',
    'dulwich'
 ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Nikos Koumbakis",
    author_email='n.koumbakis@gmail.com',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python Boilerplate for Python package.",
    entry_points={
        'console_scripts': [
            'cookiepy=cookiepy.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='cookiepy',
    name='cookiepy',
    packages=find_packages(include=['cookiepy', 'cookiepy.*']),
    setup_requires=setup_requirements + requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SpiralOutDoEu/cookiepy',
    version='0.8.1',
    zip_safe=False,
)
