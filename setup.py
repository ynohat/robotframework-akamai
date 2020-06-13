#!/usr/bin/env python

import sys
from os.path import abspath, dirname, join

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


PY3 = sys.version_info > (3,)

LIBRARY = 'AkamaiLibrary'
PACKAGE_NAME = 'robotframework-akamai'

VERSION = None
version_file = join(dirname(abspath(__file__)), 'src', LIBRARY, 'version.py')
with open(version_file) as file:
    code = compile(file.read(), version_file, 'exec')
    exec(code)

DESCRIPTION = """
Robot Framework keyword library for testing Akamai.
"""[1:-1]

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

TEST_REQUIRE = ['pytest', 'flask', 'coverage', 'flake8'] if PY3 \
    else ['pytest', 'flask', 'coverage', 'flake8', 'mock']

setup(name=LIBRARY,
      version=VERSION,
      description='Robot Framework keyword library wrapper for testing Akamai',
      long_description=DESCRIPTION,
      author='Anthony Hogg',
      author_email='anthony@hogg.fr',
      maintainer='Anthony Hogg',
      maintainer_email='anthony@hogg.fr',
      url='http://github.com/ynohat/robotframework-akamai',
      license='MIT',
      keywords='robotframework testing test automation akamai',
      platforms='any',
      classifiers=CLASSIFIERS.splitlines(),
      package_dir={'': 'src'},
      packages=[LIBRARY],
      install_requires=[
          'robotframework',
          'requests',
          'robotframework-requests'
      ],
      extras_require={
          'test': TEST_REQUIRE
      })