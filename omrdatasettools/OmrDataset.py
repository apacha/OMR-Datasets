from enum import Enum, auto
from typing import Dict


class OmrDataset(Enum):
    """
    The available OMR datasets that can be automatically downloaded with Downloader.py
    """

    Audiveris = auto()
    """ 
    The Audiveris OMR dataset from https://github.com/Audiveris/omr-dataset-tools,
    Copyright 2017 by Hervé Bitteur under AGPL-3.0 license """

    Baro = auto()
    """
    The Baro Single Stave dataset from http://www.cvc.uab.es/people/abaro/datasets.html, Copyright 2019 Arnau Baró,
    Pau Riba, Jorge Calvo-Zaragoza, and Alicia Fornés under CC-BY-NC-SA 4.0 license
    """

    Capitan = auto()
    """
    The Capitan dataset from http://grfia.dlsi.ua.es/, License unspecified, free for research purposes
    """

    CvcMuscima_MultiConditionAligned = auto()
    """
    Custom version of the CVC-MUSCIMA dataset that contains all images in grayscale, binary and with the
    following staff-line augmentations: interrupted, kanungo, thickness-variation-v1/2, y-variation-v1/2
    typeset-emulation and whitespeckles. (all data augmentations that could be aligned automatically).
    The grayscale images are different from the WriterIdentification dataset, in such a way, that they were aligned
    to the images from the Staff-Removal dataset. This is the recommended dataset for object detection, as the
    MUSCIMA++ annotations can be used with a variety of underlying images.
    See https://github.com/apacha/CVC-MUSCIMA to learn more.
    """

    CvcMuscima_StaffRemoval = auto()
    """
    The larger version of the CVC-MUSCIMA dataset for staff removal in black and white with augmentations
    from http://www.cvc.uab.es/cvcmuscima/index_database.html,
    Copyright 2012 Alicia Fornés, Anjan Dutta, Albert Gordo and Josep Lladós under CC-BY-NC-SA 4.0 license
    """

    CvcMuscima_WriterIdentification = auto()
    """
    The smaller version of the CVC-MUSCIMA dataset for writer identification in grayscale
    from http://www.cvc.uab.es/cvcmuscima/index_database.html,
    Copyright 2012 Alicia Fornés, Anjan Dutta, Albert Gordo and Josep Lladós under CC-BY-NC-SA 4.0 license
    """

    Edirom_Bargheer = auto()
    """
    Edirom dataset. All rights reserved
    """

    Edirom_FreischuetzDigital = auto()
    """
    Edirom datasets on Freischuetz from https://freischuetz-digital.de/edition.html. All rights reserved.
    """

    Fornes = auto()
    """
    The Fornes Music Symbols dataset from http://www.cvc.uab.es/~afornes/, License unspecified - citation requested
    """

    Homus_V1 = auto()
    """
    The official HOMUS dataset from http://grfia.dlsi.ua.es/homus/, License unspecified.
    """

    Homus_V2 = auto()
    """
    The improved version of the HOMUS dataset with several bugs-fixed from https://github.com/apacha/Homus.
    """

    MuscimaPlusPlus_V1 = auto()
    """
    The MUSCIMA++ dataset from https://ufal.mff.cuni.cz/muscima, Copyright 2017 Jan Hajic jr.
    under CC-BY-NC-SA 4.0 license.
    """

    MuscimaPlusPlus_V2 = auto()
    """
    The second version of the MUSCIMA++ dataset from https://github.com/OMR-Research/muscima-pp.
    """

    MuscimaPlusPlus_Images = auto()
    """
    The subset of 140 images from the CVC-MUSCIMA dataset that were used for the MUSCIMA++ dataset.
    """

    MuscimaPlusPlus_MeasureAnnotations = auto()
    """
    A sub-set of the MUSCIMA++ annotations that contains bounding-box annotations for staves, staff measures and
    system measures. It was semi-automatically constructed from existing annotations and manually verified for
    correctness. The annotations are available in a plain JSON format as well as in the COCO format.
    """

    OpenOmr = auto()
    """
    The OpenOMR Symbols dataset from https://sourceforge.net/projects/openomr/, Copyright 2013 by Arnaud F.
    Desaedeleer under GPL license.
    """

    Printed = auto()
    """
    The Printed Music Symbols dataset from https://github.com/apacha/PrintedMusicSymbolsDataset, Copyright 2017 by
    Alexander Pacha under MIT license.
    """

    Rebelo1 = auto()
    """
    The Rebelo dataset (part 1) with music symbols from http://www.inescporto.pt/~arebelo/index.php, Copyright 2017
    by Ana Rebelo under CC BY-SA 4.0 license
    """

    Rebelo2 = auto()
    """
    The Rebelo dataset (part 2) with music symbols from http://www.inescporto.pt/~arebelo/index.php, Copyright 2017
    by Ana Rebelo under CC BY-SA 4.0 license
    """

    DeepScores_V1_Extended_100_Pages = auto()
    """
    Subselection of 100 pages from the DeepScore dataset (version 1) with extended vocabulary from 
    https://tuggeluk.github.io/downloads/, License unspecified.
    """

    DeepScores_V1_Extended = auto()
    """
    The DeepScore dataset (version 1) with extended vocabulary from https://tuggeluk.github.io/downloads/,
    License unspecified.
    """

    DeepScores_V2_Dense = auto()
    """
    Subselection of 1714 pages from the DeepScore dataset (version 2) with extended vocabulary from 
    https://zenodo.org/records/4012193, under CC BY 4.0 license.
    """

    DeepScores_V2_Complete = auto()
    """
    The complete DeepScore dataset (version 2) from 
    https://zenodo.org/records/4012193, under CC BY 4.0 license.
    
    WARNING: The size of this dataset is over 80GB! 
    """

    AudioLabs_v1 = auto()
    """
    The AudioLabs v1 dataset (aka. Measure Bounding Box Annotation) from
    https://www.audiolabs-erlangen.de/resources/MIR/2019-ISMIR-LBD-Measures, Copyright 2019 by Frank Zalkow, Angel
    Villar Corrales, TJ Tsai, Vlora Arifi-Müller, and Meinard Müller under CC BY-NC-SA 4.0 license.
    """

    AudioLabs_v2 = auto()
    """
    The AudioLabs v2 dataset, enhanced with staves, staff measures and the original system measures. The annotations
    are available in csv, JSON and COCO format.
    """

    ChoiAccidentals = auto()
    """
    The Accidentals detection dataset by Kwon-Young Choi from https://www-intuidoc.irisa.fr/en/choi_accidentals/,
    License unspecified.
    """

    DoReMi = auto()
    """
    DoReMi dataset from https://github.com/steinbergmedia/DoReMi/, License unspecified.
    """

    OpenScoreLieder = auto()
    """
    OpenScore Lieder corpus from https://github.com/OpenScore/Lieder, CC-0 license.
    """

    OpenScoreStringQuartets = auto()
    """
    OpenScore StringQuartet corpus from https://github.com/OpenScore/StringQuartets, CC-0 license.
    """

    MScoreLib_All = auto()
    """
    The full MScoreLib corpus from http://mscorelib.com/, manually inputed scores by humans, License unspecified.
    """

    MScoreLib_Scriabin = auto()
    """
    MScoreLib corpus of Scriabin music, converted with SharpEye and PhotoScore, from http://mscorelib.com/, 
    License unspecified.
    """

    MScoreLib_Prokofiev = auto()
    """
    MScoreLib corpus of Prokofiev music, converted with SharpEye and PhotoScore, from http://mscorelib.com/, 
    License unspecified.
    """

    def get_dataset_download_url(self) -> str:
        """ Returns the url of the selected dataset.
            Example usage: OmrDataset.Fornes.get_dataset_download_url() """
        return self.dataset_download_urls()[self.name]

    def get_dataset_filename(self) -> str:
        """ Returns the name of the downloaded zip file of a dataset.
            Example usage: OmrDataset.Fornes.get_dataset_filename() """
        dataset_url = self.get_dataset_download_url()
        dataset_filename = dataset_url.split("/")[-1]
        return dataset_filename

    def dataset_download_urls(self) -> Dict[str, str]:
        """ Returns a mapping with all URLs, mapped from their enum keys """
        return {
            # Official URL: https://github.com/Audiveris/omr-dataset-tools/tree/master/data/input-images
            "Audiveris": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/AudiverisOmrDataset.zip",

            # Official URL: http://www.cvc.uab.es/people/abaro/datasets/MUSCIMA_ABARO.zip
            "Baro": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/BaroMuscima.zip",

            # Official URL: http://grfia.dlsi.ua.es/cm/projects/timul/databases/BimodalHandwrittenSymbols.zip
            "Capitan": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                       "BimodalHandwrittenSymbols.zip",

            # Official URL: http://www.cvc.uab.es/cvcmuscima/CVCMUSCIMA_WI.zip
            "CvcMuscima_WriterIdentification": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                               "CVCMUSCIMA_WI.zip",

            # Official URL: http://www.cvc.uab.es/cvcmuscima/CVCMUSCIMA_SR.zip
            "CvcMuscima_StaffRemoval": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                       "CVCMUSCIMA_SR.zip",

            # Official URL: https://github.com/apacha/CVC-MUSCIMA
            "CvcMuscima_MultiConditionAligned": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                                "CVCMUSCIMA_MCA.zip",

            "Edirom_Bargheer": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/Bargheer.zip",

            "Edirom_FreischuetzDigital": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                         "FreischuetzDigital.zip",

            # Official URL: http://www.cvc.uab.es/cvcmuscima/datasets/Music_Symbols.zip
            "Fornes": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/Music_Symbols.zip",

            # Official URL: http://grfia.dlsi.ua.es/homus/HOMUS.zip
            "Homus_V1": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/HOMUS.zip",

            # Official URL: https://github.com/apacha/Homus
            "Homus_V2": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/HOMUS-2.0.zip",

            # Official URL:
            # https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11372/LRT-2372/MUSCIMA-pp_v1.0.zip?sequence=1&isAllowed=y
            "MuscimaPlusPlus_V1": "https://github.com/OMR-Research/muscima-pp/releases/download/v1.0/"
                                  "MUSCIMA-pp_v1.0.zip",

            # Official URL: https://github.com/OMR-Research/muscima-pp
            "MuscimaPlusPlus_V2": "https://github.com/OMR-Research/muscima-pp/releases/download/v2.0/MUSCIMA-pp_v2.0.zip",

            "MuscimaPlusPlus_Images": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                      "CVC_MUSCIMA_PP_Annotated-Images.zip",

            "MuscimaPlusPlus_MeasureAnnotations": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                                  "MUSCIMA-pp_v1.0-measure-annotations.zip",

            # Official URL: https://sourceforge.net/projects/openomr/
            "OpenOmr": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/OpenOMR-Dataset.zip",

            "Printed": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/PrintedMusicSymbolsDataset.zip",

            "Rebelo1": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                       "Rebelo-Music-Symbol-Dataset1.zip",
            "Rebelo2": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                       "Rebelo-Music-Symbol-Dataset2.zip",

            # Official URL: "https://repository.cloudlab.zhaw.ch/artifactory/deepscores/ds_extended.zip",
            "DeepScores_V1_Extended_100_Pages": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                                "deep-scores-v1-extended-100pages.zip",
            "DeepScores_V1_Extended": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                      "deep-scores-v1-extended.zip",

            # Official URL: https://zenodo.org/records/4012193
            "DeepScores_V2_Dense": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                   "deep-scores-v2-dense.tar.gz",
            "DeepScores_V2_Complete": "https://zenodo.org/records/4012193/files/ds2_complete.tar.gz?download=1",

            # Official URL: https://www.audiolabs-erlangen.de/resources/MIR/2019-ISMIR-LBD-Measures
            "AudioLabs_v1": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/AudioLabs_v1.zip",

            "AudioLabs_v2": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/AudioLabs_v2.zip",

            # Official URL: https://www-intuidoc.irisa.fr/en/choi_accidentals/
            "ChoiAccidentals": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                               "choi_accidentals_dataset.zip",

            # Official URL: https://github.com/steinbergmedia/DoReMi/
            "DoReMi": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/DoReMi_v1.zip",

            # Official URL: https://github.com/OpenScore/Lieder
            "OpenScoreLieder": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                               "OpenScore-Lieder-Snapshot-2023-10-30.zip",

            # Official URL: https://github.com/OpenScore/StringQuartets
            "OpenScoreStringQuartets": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                       "OpenScore-StringQuartets-Snapshot-2023-10-30.zip",

            # Official URL: http://mscorelib.com/
            "MScoreLib_All": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/MScoreLib_all.zip",
            "MScoreLib_Scriabin": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                  "MScoreLib_Aleksandr_Scriabin.zip",
            "MScoreLib_Prokofiev": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/"
                                   "MScoreLib_Sergey_Prokofiev.zip",


        }
