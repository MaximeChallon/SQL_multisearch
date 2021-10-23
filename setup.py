# -*- coding: utf-8 -*-

################# To build the package and upload it ##################
# python3 setup.py sdist bdist_wheel
# twine upload dist/*
#######################################################################

from setuptools import setup
import SQL_multisearch

try:
    LONG_DESCRIPTION = open('README.md').read()
except:
    LONG_DESCRIPTION = u"Moteur de recherche dans de multiples champs d'une table SQL"

CLASSIFIERS=[
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: French",
    "Programming Language :: Python :: 3.7",
    "Topic :: Education"
]

setup(name="SQL_multisearch",
      version=SQL_multisearch.__version__,
      description="Moteur de recherche dans de multiples champs d'une table SQL",
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      author="Maxime Challon",
      author_email="maxime.challon@gmail.com",
      keywords="SQL search ranking",
      classifiers=CLASSIFIERS,
      packages=["SQL_multisearch"],
      test_suite='nose.collector',
      tests_require=['nose'])