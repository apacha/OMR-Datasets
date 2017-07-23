# [Optical Music Recognition Datasets](https://apacha.github.io/OMR-Datasets/)

This repository contains a collection of many datasets used for various Optical Music Recognition tasks, including staff-line detection and removal, training of Convolutional Neuronal Networks (CNNs) or validating existing systems by comparing your system with a known ground-truth.

Note that most datasets have been developed by researchers and using their dataset requires accepting a certain license and/or citing their respective publications, as indicated for each dataset. Most datasets link to the official website, where you can download the dataset.

Datasets referenced from this repository:

* [Handwritten Online Musical Symbols (HOMUS)](#handwritten-online-musical-symbols-homus)
* [Music Score Classification Dataset](#music-score-classification-dataset)
* [CVC-MUSCIMA](#cvc-muscima)
* [MUSCIMA++](#muscima)
* [MuseScore Monophonic MusicXML Dataset](#musescore-monophonic-musicxml-dataset)
* [Rebelo Dataset](#rebelo-dataset)
* [Fornes Dataset](#fornes-dataset)
* [Audiveris OMR](#audiveris-omr)
* [Gamera Project](#gamera-project)
* [Byrd Dataset](#byrd-dataset)

# Handwritten Online Musical Symbols (HOMUS)

**Official website**: [http://grfia.dlsi.ua.es/homus/](http://grfia.dlsi.ua.es/homus/)
 
[![License](https://img.shields.io/badge/License-Unknown-red.svg)](http://grfia.dlsi.ua.es/homus/)

**Summary**: The Handwritten Online Musical Symbols (HOMUS) dataset is a reference corpus with around 15000 samples for research on the recognition of online handwritten music notation. For each sample, the individual strokes that the musicians wrote on a Samsung Tablet using a stylus were recorded and can be used in online and offline scenarios.

**Scientific Publication**: J. Calvo-Zaragoza and J. Oncina, "Recognition of Pen-Based Music Notation: The HOMUS Dataset," 2014 22nd International Conference on Pattern Recognition, Stockholm, 2014, pp. 3038-3043. [DOI: 10.1109/ICPR.2014.524](http://dx.doi.org/10.1109/ICPR.2014.524)

**Example**:

![Example of HOMUS dataset](HOMUS/HOMUS_Samples.png)


*Remarks*: The original dataset contains around 20 artifacts and misclassifications that were reported to the authors and [corrected by Alexander Pacha](https://github.com/apacha/Homus). 


# Music Score Classification Dataset

**Official website**: [https://github.com/apacha/MusicScoreClassifier](https://github.com/apacha/MusicScoreClassifier) 

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

**Summary**: A dataset of 2000 images, containing 1000 images of music scores and 1000 images of other objects including text documents. The images were taken with a smartphone camera from various angles and different lighting conditions.

**Scientific Publication**: Under review

**Example**:

![Example of MusicScoreClassifier dataset](MusicScoreClassifier/MusicScoreClassifierExamples.png)

# CVC-MUSCIMA

**Official website**: [http://www.cvc.uab.es/cvcmuscima/index_database.html](http://www.cvc.uab.es/cvcmuscima/index_database.html)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-blue.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Summary**: The CVC-MUSCIMA database contains handwritten music score images, which has been specially designed for writer identification and staff removal tasks. The database contains 1,000 music sheets written by 50 different musicians. All of them are adult musicians, in order to ensure that they have their own characteristic handwriting style. Each writer has transcribed the same 20 music pages, using the same pen and the same kind of music paper (with printed staff lines). The set of the 20 selected music sheets contains music scores for solo instruments and music scores for choir and orchestra.

**Scientific Publication**: Alicia Fornés, Anjan Dutta, Albert Gordo, Josep Lladós. CVC-MUSCIMA: A Ground-truth of Handwritten Music Score Images for Writer Identification and Staff Removal. International Journal on Document Analysis and Recognition, Volume 15, Issue 3, pp 243-251, 2012. [DOI: 10.1007/s10032-011-0168-2](http://dx.doi.org/10.1007/s10032-011-0168-2)

**Example**:

![Example of CVC MUSCIMA dataset](CVC-MUSCIMA/p014_Gray.png)

# MUSCIMA++

**Official website**: [https://ufal.mff.cuni.cz/muscima](https://ufal.mff.cuni.cz/muscima)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-blue.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Summary**: MUSCIMA++ is a dataset of handwritten music notation for musical symbol detection that is based on the MUSCIMA dataset. It contains 91255 symbols, consisting of both notation primitives and higher-level notation objects, such as key signatures or time signatures. There are 23352 notes in the dataset, of which 21356 have a full notehead, 1648 have an empty notehead, and 348 are grace notes. Composite objects, such as notes, are captured through explicitly annotated relationships of the notation primitives (noteheads, stems, beams...). This way, the annotation provides an explicit bridge between the low-level and high-level symbols described in Optical Music Recognition literature.

**Scientific Publication**: Jan Hajič jr., Pavel Pecina. In Search of a Dataset for Handwritten Optical Music Recognition: Introducing MUSCIMA++. CoRR, arXiv:1703.04824, 2017. https://arxiv.org/abs/1703.04824

**Example**:

![Example of MUSCIMA++ dataset](MUSCIMA-pp/intro_screenshot_1.png)

*Remarks*: Since this dataset is derived from the MUSCIMA dataset, using it requires to reference both works.

# MuseScore Monophonic MusicXML Dataset

**Official website**: [https://github.com/eelcovdw/mono-musicxml-dataset]()

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

**Summary**: TBD

**Scientific Publication**: Eelco van der Wel, Karen Ullrich. Optical Music Recognition with Convolutional Sequence-to-Sequence Models. CoRR, arXiv:1707.04877, 2017. https://arxiv.org/abs/1707.04877

**Example**: TBD



# Rebelo Dataset

**Official websites**: [http://www.inescporto.pt/~arebelo/index.php](http://www.inescporto.pt/~arebelo/index.php) and [http://www.inescporto.pt/~jsc/projects/OMR/](http://www.inescporto.pt/~jsc/projects/OMR/)

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-blue.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

**Summary**: Three datasets of perfect and scanned music symbols including an extensive set of synthetically modified images for staff-line detection and removal.

**Scientific Publication**: A. Rebelo, G. Capela, and J. S. Cardoso, "Optical recognition of music symbols: A comparative study" in International Journal on Document Analysis and Recognition, vol. 13, no. 1, pp. 19-31, 2010. [DOI: 10.1007/s10032-009-0100-1](http://dx.doi.org/10.1007/s10032-009-0100-1)

**Examples**:

![Example of Rebelo dataset](RebeloDataset/Samples.png)
![Example of Rebelo dataset](RebeloDataset/img043-nostafflines.png)


*Remarks*: The dataset is usually only available upon request, but with written permission of Ana Rebelo I hereby make the datasets available under a permissive CC-BY-SA license, which allows you to use it freely given you properly mention her work by citing the above mentioned publication: [Download the dataset](https://owncloud.tuwien.ac.at/index.php/s/g3q0COsfPqbDUAW).


# Fornes Dataset
**Official website**: [http://www.cvc.uab.es/~afornes/](http://www.cvc.uab.es/~afornes/)

[![License](https://img.shields.io/badge/License-Unknown-red.svg)](http://grfia.dlsi.ua.es/homus/)

**Summary**: A dataset of 4100 black and white symbols of 7 different symbol classes: flat, natural, sharp, double-sharp, c-clef, g-clef, f-clef. 

**Scientific Publication**: A.Fornés and J.Lladós and G. Sanchez, "Old Handwritten Musical Symbol Classification by a Dynamic Time Warping Based Method", in Graphics Recognition: Recent Advances and New Opportunities. Liu, W. and Lladós, J. and Ogier, J.M. editors, Lecture Notes in Computer Science, Volume 5046, Pages 51-60, Springer-Verlag Berlin, Heidelberg, 2008. [DOI: 10.1007/978-3-540-88188-9_6
](http://dx.doi.org/10.1007/978-3-540-88188-9_6)

**Example**:

![Example of the Fornes Dataset](FornesDataset/music_accidentals.png)
![Example of the Fornes Dataset](FornesDataset/music_clefs.png)

# Audiveris OMR

**Official website**: [https://github.com/Audiveris/omr-dataset-tools](https://github.com/Audiveris/omr-dataset-tools)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-AGPL--3.0-green.svg)](https://www.gnu.org/licenses/agpl-3.0.en.html)

**Summary**: A collection of four music sheets with approximately 800 annotated music symbols. The [DeepScore project](https://www.zhaw.ch/no_cache/en/research/people-publications-projects/detail-view-project/projekt/2895/) in cooperation with the ZHAW targets towards [automatically generating these images](https://github.com/Audiveris/omr-dataset-tools/wiki/Synthetic-Images) and the annotations from MuseScore or Lilypond documents. 

**Example**:

![Example of the Audiveris OMR Dataset](Audiveris-OMR/sample.png)

# Gamera MusicStaves Toolkit

**Official website**: [http://music-staves.sf.net/ and https://github.com/hsnr-gamera](http://music-staves.sf.net/ and https://github.com/hsnr-gamera)

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-yellow.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

**Summary**: The Synthetic Score Database by Christoph Dalitz that contains 32 scores that have been computer generated with different music typesetting programs. It contains ground truth data and is suitable for the deformations implemented in the toolkit.

**Scientific Publication**: C. Dalitz, M. Droettboom, B. Pranzas, I. Fujinaga: A Comparative Study of Staff Removal Algorithms. IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 30, no. 5, pp. 753-766 (2008) [DOI: 10.1109/TPAMI.2007.70749](http://dx.doi.org/10.1109/TPAMI.2007.70749)

**Example**:

![Example of the Gamera MusicStaves Dataset](GameraMusicStavesToolkit/bach.png)


# Byrd Dataset

**Official website**: [http://www.diku.dk/hjemmesider/ansatte/simonsen/suppmat/jnmr/](http://www.diku.dk/hjemmesider/ansatte/simonsen/suppmat/jnmr/)

[![License](https://img.shields.io/badge/License-Unknown-red.svg)](http://grfia.dlsi.ua.es/homus/) (Authors want to be contacted)

**Summary**: A small dataset of 34 high quality images with individual music score pages of increasing difficulty. 

**Scientific Publication**: Donald Byrd & Jakob Grue Simonsen: "Towards a Standard Testbed for Optical Music Recognition: Definitions, Metrics, and Page Images". Journal of New Music Research, vol 44, nr.3, pages 169-195, 2015. [DOI: 10.1080/09298215.2015.1045424](http://dx.doi.org/10.1080/09298215.2015.1045424)

**Example**:

![Example of the Byrd Dataset](ByrdDataset/Sample.png)

