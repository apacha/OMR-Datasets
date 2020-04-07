.. py:module:: omrdatasettools

Image Generators
================

.. py:currentmodule:: omrdatasettools.AudiverisOmrImageGenerator

:py:mod:`AudiverisOmrImageGenerator` Module
-------------------------------------------

.. autoclass:: AudiverisOmrImageGenerator

.. automethod:: AudiverisOmrImageGenerator.extract_symbols


.. py:currentmodule:: omrdatasettools.CapitanImageGenerator

:py:mod:`CapitanImageGenerator` Module
--------------------------------------

.. autoclass:: CapitanImageGenerator

.. automethod:: CapitanImageGenerator.create_capitan_images


.. py:currentmodule:: omrdatasettools.HomusImageGenerator

:py:mod:`HomusImageGenerator` Module
------------------------------------

.. autoclass:: HomusImageGenerator

.. automethod:: HomusImageGenerator.create_images

.. automethod:: HomusImageGenerator.add_arguments_for_homus_image_generator


:py:mod:`HomusSymbol` Module
----------------------------

.. autoclass:: HomusSymbol

.. automethod:: HomusSymbol.initialize_from_string

.. automethod:: HomusSymbol.draw_into_bitmap

.. automethod:: HomusSymbol.draw_onto_canvas


.. py:currentmodule:: omrdatasettools.MeasureVisualizer

:py:mod:`MeasureVisualizer` Module
----------------------------------

This class can be used to generate visualizations of measure annotations, such as this one for the Muscima++ dataset:

.. image:: images/muscima-pp-measures.png

.. autoclass:: MeasureVisualizer

.. automethod:: MeasureVisualizer.draw_bounding_boxes_for_all_images_in_directory

.. automethod:: MeasureVisualizer.draw_bounding_boxes_into_image


.. py:currentmodule:: omrdatasettools.MuscimaPlusPlusSymbolImageGenerator

:py:mod:`MuscimaPlusPlusSymbolImageGenerator` Module
----------------------------------------------------

.. autoclass:: MuscimaPlusPlusSymbolImageGenerator

.. automethod:: MuscimaPlusPlusSymbolImageGenerator.extract_and_render_all_symbol_masks
