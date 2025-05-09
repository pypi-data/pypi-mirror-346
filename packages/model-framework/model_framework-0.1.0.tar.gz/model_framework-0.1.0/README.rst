.. image:: https://img.shields.io/pypi/v/model-framework.svg?style=flat
   :target: https://pypi.org/project/model-framework/
   :alt: Latest PyPI version

.. image:: https://readthedocs.org/projects/mframework/badge/?version=latest
    :target: https://mframework.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-Apache%202-blue.svg
    :target: https://github.com/airinnova/model-framework/blob/master/LICENSE.txt
    :alt: License

.. image:: https://travis-ci.org/airinnova/model-framework.svg?branch=master
    :target: https://travis-ci.org/airinnova/model-framework
    :alt: Build status

.. image:: https://codecov.io/gh/airinnova/model-framework/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/airinnova/model-framework
    :alt: Coverage

|

.. image:: https://raw.githubusercontent.com/airinnova/model-framework/master/docs/source/_static/images/logo.png
   :target: https://github.com/airinnova/model-framework/
   :alt: logo

⚠ **Work in progress!** This project is in an early prototyping phase.

What is 'model-framework'?
==========================

..
    ----------

Model-framework is a framework to build simple to use Python interfaces for complex models. For instance, a structural analysis tool (like `FramAT <https://github.com/airinnova/framat>`_) requires a number of user inputs parameters, for instance, for general settings, material or loads. It can be cumbersome to develop a consistent user interface for such a tool which has a large number of settings. Model-framework helps to build good Python user API's for complex models. In particular it aims to improve the following aspects of the developer and user experiences.

* Providing a simple to understand Python API to build and interact with complex models
* Enforcing API consistency
* User input validation
* Full API documentation through automatic documentation generation
* Flexible model extensibility
* Clear separation between user input and solution routines

..
    ----------

Please refer do the `documentation <https://mframework.readthedocs.io>`_ for more information.

Installation
============

*Model-Framework* is available on `PyPI <https://pypi.org/project/model-framework/>`_ and may simply be installed with

.. code::

    pip install model-framework

License
=======

**License:** Apache-2.0
