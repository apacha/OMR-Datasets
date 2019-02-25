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

.. code-block:: console

    pip install omrdatasettools

Example usage
-------------

Consider you want to work with the `HOMUS dataset <http://grfia.dlsi.ua.es/homus/>`_, you can use the following script to download the dataset:

.. code-block:: python

    from omrdatasettools.downloaders.HomusDatasetDownloader import HomusDatasetDownloader

    dataset_downloader = HomusDatasetDownloader("raw_dataset_destination_path")
    dataset_downloader.download_and_extract_dataset()

Once the download has completed, you may want to work with images, instead of textual descriptions. The package `omrdatasettools.image_generators` contains the appropriate tools for doing so:

.. code-block:: python

    from omrdatasettools.image_generators.HomusImageGenerator import HomusImageGenerator

    HomusImageGenerator.create_images(raw_data_directory="raw_dataset_destination_path",
                                      destination_directory="dataset_destination_path",
                                      stroke_thicknesses=[3],
                                      canvas_width=96,
                                      canvas_height=192,
                                      staff_line_spacing=14,
                                      staff_line_vertical_offsets=[24])

Note that the image generator has a lot of options that define how the images will be generated, but to stay with this example, it will create image of the size 192x96, draw the symbols with a line-thickness of three pixels, superimpose five staff-lines with 14 pixel space inbetween, beginning at 24 pixels from the top.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   downloaders/index.rst
   image_generators/index.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
