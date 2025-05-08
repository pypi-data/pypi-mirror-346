
.. image:: https://readthedocs.org/projects/aws-organizations/badge/?version=latest
    :target: https://aws-organizations.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/aws_organizations-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/aws_organizations-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/aws_organizations-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/aws_organizations-project

.. image:: https://img.shields.io/pypi/v/aws-organizations.svg
    :target: https://pypi.python.org/pypi/aws-organizations

.. image:: https://img.shields.io/pypi/l/aws-organizations.svg
    :target: https://pypi.python.org/pypi/aws-organizations

.. image:: https://img.shields.io/pypi/pyversions/aws-organizations.svg
    :target: https://pypi.python.org/pypi/aws-organizations

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/aws_organizations-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/aws_organizations-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://aws-organizations.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://aws-organizations.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/aws_organizations-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/aws_organizations-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/aws_organizations-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/aws-organizations#files


Welcome to ``aws_organizations`` Documentation
==============================================================================
.. image:: https://aws-organizations.readthedocs.io/en/latest/_static/aws_organizations-logo.png
    :target: https://aws-organizations.readthedocs.io/en/latest/

AWS Organizations SDK enhancement.

**Features**

1. Enhanced Boto3 API
    - Provides improved boto3 APIs for AWS Organizations with:
    - Type hints for better IDE support
    - Simplified pagination handling
    - Streamlined access to organization, organizational units, and account information
    - Clear hierarchy relationship queries

2. Object-Oriented Organization Structure
    - The ``OrgStructure`` class provides a tree-based container for AWS organization data:
    - Tree structure representation of your AWS organization
    - Easy navigation through organization hierarchy
    - Utility methods for finding and analyzing organization components
    - Multiple export formats for visualization and analysis


.. _install:

Install
------------------------------------------------------------------------------

``aws_organizations`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install aws-organizations

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade aws-organizations
