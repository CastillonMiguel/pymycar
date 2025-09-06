pyMyCar
=======

.. image:: https://raw.githubusercontent.com/CastillonMiguel/pymycar/main/docs/source/_static/logo.png
   :target: https://pymycar.readthedocs.io/en/latest/index.html
   :alt: pymycar


Welcome to **pyMyCar**. `documentation <https://pymycar.readthedocs.io/en/latest/index.html>`_

.. image:: https://readthedocs.org/projects/pymycar/badge/?version=latest
    :target: https://pymycar.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
    
.. image:: https://img.shields.io/pypi/v/pymycar
    :target: https://pypi.org/project/pymycar/
    :alt: PyPI Version

.. image:: https://img.shields.io/pypi/dm/pymycar.svg?label=Pypi%20downloads
    :target: https://pypi.org/project/pymycar/
    :alt: PyPI Downloads

.. image:: https://img.shields.io/github/license/CastillonMiguel/pymycar
    :target: https://github.com/CastillonMiguel/pymycar/blob/main/LICENSE
    :alt: License

.. image:: https://github.com/CastillonMiguel/pymycar/actions/workflows/testing.yml/badge.svg
    :target: https://github.com/CastillonMiguel/pymycar/actions/workflows/testing.yml   
    :alt: Unit Testing
 
.. image:: https://deepwiki.com/badge.svg
   :target: https://deepwiki.com/CastillonMiguel/pymycar
   :alt: Ask DeepWiki

Introduction
------------
The **pyMyCar** project is a comprehensive Python library designed to facilitate the analysis and simulation of vehicle dynamics. This package provides tools to explore, simulate, and optimize various suspension configurations, enhancing vehicle performance and safety.

Installation Instructions (Conda Environment)
---------------------------------------------
To install pyMyCar and its dependencies in a dedicated conda environment, follow these steps:

1. Create a new conda environment (recommended for isolation):

   .. code-block:: sh

      conda create -n pymycar-env

2. Activate the environment:

   .. code-block:: sh

      conda activate pymycar-env

3. Install required packages (`pandas`, `pyvista`) from the `conda-forge` channel:

   .. code-block:: sh

      conda install -c conda-forge pyvista pandas

4. Install pyMyCar from PyPI using pip:

   .. code-block:: sh

      pip install pymycar

These instructions ensure all dependencies are installed in a clean, isolated conda environment. Always activate `pymycar-env` before working with this project.


Examples
--------
There are numerous examples available to demonstrate the usage of pyMyCar for various vehicle dynamics simulations. These examples cover different scenarios such as suspension analysis, vehicle stability, and more complex dynamics simulations. Explore the examples in the `documentation <https://pymycar.readthedocs.io/en/latest/index.html>`_ to learn more.

API Documentation
-----------------
For detailed API documentation, including class references, function definitions, and usage examples, please refer to the `API documentation <https://pymycar.readthedocs.io/en/latest/api/index.html>`_.

You can also explore the project on DeepWiki — an AI-powered, interactive knowledge base built from the code and documentation: `Explore pyMyCar on DeepWiki <https://deepwiki.com/CastillonMiguel/pymycar>`_

Contributions and Feedback
--------------------------
We welcome contributions and feedback from the community to enhance the code's functionality, reliability, and user experience.To get started, please review our `Contributing Guidelines <https://pymycar.readthedocs.io/en/latest/extras/DeveloperNotes/main.html>`_ to share your insights and collaborate with fellow developers.

Thank you for choosing our pyMyCar simulation code. We trust this tool will prove invaluable in advancing your understanding of vehicle dynamics and its practical applications.