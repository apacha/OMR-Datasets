.. py:module:: omrdatasettools.downloaders.AudiverisOmrDatasetDownloader
.. py:currentmodule:: omrdatasettools.downloaders.AudiverisOmrDatasetDownloader

:py:mod:`AudiverisOmrDatasetDownloader` Module
==============================================

The :py:mod:`~AudiverisOmrDatasetDownloader` module provides methods for downloading the
Audiveris OMR dataset.

Examples
--------

The following script downloads the Audiveris OMR dataset

Download
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from omrdatasettools.downloaders.AudiverisOmrDatasetDownloader import AudiverisOmrDatasetDownloader

    dataset = AudiverisOmrDatasetDownloader("images")
    dataset.download_and_extract_dataset()


Reference
---------------

.. autoclass:: omrdatasettools.downloaders.AudiverisOmrDatasetDownloader.AudiverisOmrDatasetDownloader

.. automethod:: omrdatasettools.downloaders.AudiverisOmrDatasetDownloader.AudiverisOmrDatasetDownloader.download_and_extract_dataset
