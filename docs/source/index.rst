.. OMR Dataset Tools documentation master file, created by
   sphinx-quickstart on Fri Aug 25 17:19:52 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OMR Dataset Tools's documentation!
=============================================

This is a collection of tools for working with the datasets referenced from this repository, including common
function like:

* Downloading the datasets and extracting them
* Processing specific datasets, e.g. generating images from the raw HOMUS dataset.

The package `omrdatasettools.downloaders` contains one class per dataset, that is capable of downloading
and extracting the respective dataset. To see how they work, each of them has a main-function that can
be executed as it is.

A pip-package is available so you can include the tools conveniently into your projects by using

    $ pip install omrdatasettools


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reference/index.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
