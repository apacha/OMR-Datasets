Changelog
=========

1.3.0
-----
Added download capabilities of DeepScores V1 with extended vocabulary and
opened the downloader, so you can download custom datasets, as well as utilize
other methods from it that were previously private.

1.2.2
-----
Fixed incorrect import statement in `__init__.py`

1.2.1
-----
Fixed dependency problem during `setup.py` that prevented the package from being 
installed if the dependent libraries are not yet installed (which defeats
the purpose of declaring dependencies in setup.py).
Changing to semantic versioning with three numbers. 
1.2 is now considered 1.2.0.

1.2
---
Attempting to declare dependencies in `setup.py` properly

1.1
---
Updated MuscimaPlusPlusSymbolImageGenerator to work with MUSCIMA++ 2.0.
Added quality-of-life improvement suggested by @yvan674 to make importing 
common classes such as the downloader easier.


1.0
---
Dramatically simplified the tools for downloading datasets. 
Removed mostly unused code and re-organized project structure and documentation.

0.19
----
New Image generator that can take MUSCIMA++ v2.0 images and 
generate masks for instance segmentation of staffs, as well as
masks for semantic segmentation for all objects.

0.18
----
Changing MUSCIMA++ Downloader to accept a string instead of integer for enabling
future versioning of the dataset beyond integers, e.g., "2.1".

Previous releases
-----------------
For information on previous releases, check out the [Github Repository](https://github.com/apacha/OMR-Datasets/releases)