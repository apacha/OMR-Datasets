# Large Scale Optical Music Recognition Database Project

This repository contains a collection of many datasets used for various Optical Music Recognition tasks, including training of Convolutional Neuronal Networks (CNNs), validating existing systems or comparing your system with a known ground-truth.

Note that most datasets have been developed by researcher and using their dataset requires accepting a certain license and/or citing their respective publications, as indicated for each dataset. Most datasets link to the official website, where you can download the dataset, but also contain a link to a mirror, in case the dataset disappears for some reasons.

Finally, there are scripts available, that automatically download the dataset and provide a unified interface for downloading, extracting and handling the different datasets.

Datasets inside this repository:

* [Handwritten Online Musical Symbols (HOMUS)](#handwritten-online-musical-symbols-homus)
* [Music Score Classification Dataset](#music-score-classification-dataset)
* CVC-MUSCIMA
* MUSCIMA++
* Audiveris OMR
* Rebelo Dataset

# Handwritten Online Musical Symbols (HOMUS)

**Official website**: http://grfia.dlsi.ua.es/homus/
 
[![License](https://img.shields.io/badge/License-Unknown-yellow.svg)](http://grfia.dlsi.ua.es/homus/)

**Summary**: The goal of the Handwritten Online Musical Symbols (HOMUS) dataset is to provide a reference corpus with around 15000 samples for research on the recognition of online handwritten music notation. For each sample, the individual strokes that the musicians wrote on a Samsung Tablet using a stylus were recorded and can be used in online and offline scenarios.

**Scientific Publication**: 

*Remarks*: The original dataset contains around 20 artifacts and misclassifications that were [corrected by Alexander Pacha](https://github.com/apacha/Homus). The corrections are included in version 2.0.


# Music Score Classification Dataset

**Official website**: https://github.com/apacha/MusicScoreClassifier 

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Summary**: A dataset of 2000 images, containing 1000 images of music scores and 1000 images of other objects including text documents. The images were taken with a smartphone camera from various angles and different lighting conditions. 