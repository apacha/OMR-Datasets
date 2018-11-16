import argparse
import os
from enum import Enum

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class CvcMuscimaDataset(Enum):
    WriterIdentification = 1

    StaffRemoval = 2

    # Custom version of the two above datasets, that contains all images in grayscale, binary and with
    # the following staff-line augmentations: interrupted, kanungo, thickness-variation-v1/2, y-variation-v1/2,
    # typeset-emulation and whitespeckles.
    # The grayscale images are different from the WriterIdentification dataset, in such a way, that they were aligned
    # to the images from the Staff-Removal dataset.
    MultiConditionAligned = 3


class CvcMuscimaDatasetDownloader(DatasetDownloader):
    """ Downloads the CVC-MUSCIMA dataset
        http://www.cvc.uab.es/cvcmuscima/index_database.html
        Copyright 2012 Alicia Fornés, Anjan Dutta, Albert Gordo and Josep Lladós under CC-BY-NC-SA 4.0 license
    """

    def __init__(self, dataset: CvcMuscimaDataset = CvcMuscimaDataset.WriterIdentification):
        self.dataset = dataset

    def get_dataset_download_url(self) -> str:
        if self.dataset is CvcMuscimaDataset.WriterIdentification:
            # Official URL: "http://www.cvc.uab.es/cvcmuscima/CVCMUSCIMA_WI.zip"
            return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/CVCMUSCIMA_WI.zip"
        if self.dataset is CvcMuscimaDataset.StaffRemoval:
            # Official URL: "http://www.cvc.uab.es/cvcmuscima/CVCMUSCIMA_SR.zip"
            return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/CVCMUSCIMA_SR.zip"
        if self.dataset is CvcMuscimaDataset.MultiConditionAligned:
            return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/CVCMUSCIMA_MCA.zip"

    def get_dataset_filename(self) -> str:
        if self.dataset is CvcMuscimaDataset.WriterIdentification:
            return "CVCMUSCIMA_WI.zip"
        if self.dataset is CvcMuscimaDataset.StaffRemoval:
            return "CVCMUSCIMA_SR.zip"
        if self.dataset is CvcMuscimaDataset.MultiConditionAligned:
            return "CVCMUSCIMA_MCA.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading CVC-MUSCIMA Dataset ({0})...".format(self.dataset))
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting CVC-MUSCIMA Dataset...")
        self.extract_dataset(os.path.abspath(destination_directory))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/cvc_muscima",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = CvcMuscimaDatasetDownloader(CvcMuscimaDataset.MultiConditionAligned)
    dataset.download_and_extract_dataset(flags.dataset_directory)
