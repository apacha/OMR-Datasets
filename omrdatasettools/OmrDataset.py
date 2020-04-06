from enum import Enum, auto
from typing import Dict


class OmrDataset(Enum):
    """
        The available OMR datasets that can be automatically downloaded with Downloader.py
    """

    Audiveris = auto()  # The Audiveris OMR dataset from https://github.com/Audiveris/omr-dataset-tools, Copyright 2017 by Hervé Bitteur under AGPL-3.0 license
    Baro = auto()  # The Baro Single Stave dataset from http://www.cvc.uab.es/people/abaro/datasets.html, Copyright 2019 Arnau Baró, Pau Riba, Jorge Calvo-Zaragoza, and Alicia Fornés under CC-BY-NC-SA 4.0 license
    Capitan = auto()  # The Capitan dataset from http://grfia.dlsi.ua.es/, License unspecified, free for research purposes

    # The CVC-MUSCIMA dataset from http://www.cvc.uab.es/cvcmuscima/index_database.html
    # Copyright 2012 Alicia Fornés, Anjan Dutta, Albert Gordo and Josep Lladós under CC-BY-NC-SA 4.0 license
    # In three different version:
    # - The smaller version for writer identification in grayscale
    # - The larger version for staff removal in black and white with augmentations
    # - Custom version of the two above datasets, that contains all images in grayscale, binary and with the
    #   following staff-line augmentations: interrupted, kanungo, thickness-variation-v1/2, y-variation-v1/2
    #   typeset-emulation and whitespeckles. (all data augmentations that could be aligned automatically)
    #   The grayscale images are different from the WriterIdentification dataset, in such a way, that they were aligned
    #   to the images from the Staff-Removal dataset. This is the recommended dataset for object detection, as the
    #   MUSCIMA++ annotations can be used with a variety of underlying images
    CvcMuscima_WriterIdentification = auto()
    CvcMuscima_StaffRemoval = auto()
    CvcMuscima_MultiConditionAligned = auto()

    # Edirom datasets: All rights reserved
    # - Freischuetz: https://freischuetz-digital.de/edition.html, All rights reserved
    Edirom_Bargheer = auto()
    Edirom_FreischuetzDigital = auto()

    # The Fornes Music Symbols dataset from http://www.cvc.uab.es/~afornes/, License unspecified - citation requested
    Fornes = auto()

    # The HOMUS dataset from http://grfia.dlsi.ua.es/homus/, License unspecified.
    # - V1 = Official version,
    # - V2 = Version with bug-fixes
    Homus_V1 = auto()
    Homus_V2 = auto()

    # The MUSCIMA++ dataset from https://ufal.mff.cuni.cz/muscima, Copyright 2017 Jan Hajic jr. under CC-BY-NC-SA 4.0 license
    MuscimaPlusPlus_V1 = auto()
    MuscimaPlusPlus_V2 = auto()

    # The OpenOMR Symbols dataset from https://sourceforge.net/projects/openomr/, Copyright 2013 by Arnaud F. Desaedeleer under GPL license
    OpenOmr = auto()

    # The Printed Music Symbols dataset from https://github.com/apacha/PrintedMusicSymbolsDataset, Copyright 2017 by Alexander Pacha under MIT license
    Printed = auto()

    # The Rebelo datasets with music symbols from http://www.inescporto.pt/~arebelo/index.php, Copyright 2017 by Ana Rebelo under CC BY-SA 4.0 license
    Rebelo1 = auto()
    Rebelo2 = auto()

    def get_dataset_download_url(self) -> str:
        return self.dataset_download_urls()[self.name]

    def get_dataset_filename(self) -> str:
        return self.dataset_file_names()[self.name]

    def dataset_download_urls(self) -> Dict[str, str]:
        return {
            # Official URL: https://github.com/Audiveris/omr-dataset-tools/tree/master/data/input-images
            "Audiveris": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/AudiverisOmrDataset.zip",

            # Official URL: http://www.cvc.uab.es/people/abaro/datasets/MUSCIMA_ABARO.zip
            "Baro": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/BaroMuscima.zip",

            # Official URL: http://grfia.dlsi.ua.es/cm/projects/timul/databases/BimodalHandwrittenSymbols.zip
            "Capitan": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/BimodalHandwrittenSymbols.zip",

            # Official URL: http://www.cvc.uab.es/cvcmuscima/CVCMUSCIMA_WI.zip
            "CvcMuscima_WriterIdentification": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/CVCMUSCIMA_WI.zip",

            # Official URL: http://www.cvc.uab.es/cvcmuscima/CVCMUSCIMA_SR.zip
            "CvcMuscima_StaffRemoval": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/CVCMUSCIMA_SR.zip",

            # Official URL: https://github.com/apacha/CVC-MUSCIMA
            "CvcMuscima_MultiConditionAligned": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/CVCMUSCIMA_MCA.zip",

            "Edirom_Bargheer": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/Bargheer.zip",

            "Edirom_FreischuetzDigital": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/FreischuetzDigital.zip",

            # Official URL: http://www.cvc.uab.es/cvcmuscima/datasets/Music_Symbols.zip
            "Fornes": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/Music_Symbols.zip",

            # Official URL: http://grfia.dlsi.ua.es/homus/HOMUS.zip
            "Homus_V1": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/HOMUS.zip",

            # Official URL: https://github.com/apacha/Homus
            "Homus_V2": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/HOMUS-2.0.zip",

            # Official URL: https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11372/LRT-2372/MUSCIMA-pp_v1.0.zip?sequence=1&isAllowed=y
            "MuscimaPlusPlus_V1": "https://github.com/OMR-Research/muscima-pp/releases/download/v1.0/MUSCIMA-pp_v1.0.zip",

            # Official URL: https://github.com/OMR-Research/muscima-pp
            "MuscimaPlusPlus_V2": "https://github.com/OMR-Research/muscima-pp/releases/download/v2.0/MUSCIMA-pp_v2.0.zip",

            "MuscimaPlusPlus_Images": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/CVC_MUSCIMA_PP_Annotated-Images.zip",

            "MuscimaPlusPlus_MeasureAnnotations": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/MUSCIMA-pp_v1.0-measure-annotations.zip",

            # Official URL: https://sourceforge.net/projects/openomr/
            "OpenOmr": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/OpenOMR-Dataset.zip",

            "Printed": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/PrintedMusicSymbolsDataset.zip",

            "Rebelo1": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/Rebelo-Music-Symbol-Dataset1.zip",
            "Rebelo2": "https://github.com/apacha/OMR-Datasets/releases/download/datasets/Rebelo-Music-Symbol-Dataset2.zip",
        }

    def dataset_file_names(self) -> Dict[str,str]:
        return {
            "Audiveris": "AudiverisOmrDataset.zip",
            "Baro": "BaroMuscima.zip",
            "Capitan": "BimodalHandwrittenSymbols.zip",
            "CvcMuscima_WriterIdentification": "CVCMUSCIMA_WI.zip",
            "CvcMuscima_StaffRemoval": "CVCMUSCIMA_SR.zip",
            "CvcMuscima_MultiConditionAligned": "CVCMUSCIMA_MCA.zip",
            "Edirom_Bargheer": "Bargheer.zip",
            "Edirom_FreischuetzDigital": "FreischuetzDigital.zip",
            "Fornes": "Music_Symbols.zip",
            "Homus_V1": "HOMUS.zip",
            "Homus_V2": "HOMUS-2.0.zip",
            "MuscimaPlusPlus_V1": "MUSCIMA-pp_v1.0.zip",
            "MuscimaPlusPlus_V2": "MUSCIMA-pp_v2.0.zip",
            "MuscimaPlusPlus_Images": "CVC_MUSCIMA_PP_Annotated-Images.zip",
            "MuscimaPlusPlus_MeasureAnnotations": "MUSCIMA-pp_v1.0-measure-annotations.zip",
            "OpenOmr": "OpenOMR-Dataset.zip",
            "Printed": "PrintedMusicSymbolsDataset.zip",
            "Rebelo1": "Rebelo-Music-Symbol-Dataset1.zip",
            "Rebelo2": "Rebelo-Music-Symbol-Dataset2.zip",
        }