import argparse
import os
from enum import Enum, auto

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader

class CvcMuscimaDataset(Enum):
    WriterIdentification = auto()
    StaffRemoval = auto()

class CvcMuscimaDatasetDownloader(DatasetDownloader):
    """ Downloads the CVC-MUSCIMA dataset
        http://www.cvc.uab.es/cvcmuscima/index_database.html
        Copyright 2012 Alicia Fornés, Anjan Dutta, Albert Gordo and Josep Lladós under CC-BY-NC-SA 4.0 license
    """

    def __init__(self, destination_directory: str, dataset: CvcMuscimaDataset = CvcMuscimaDataset.WriterIdentification):
        """
        Create and initializes a new dataset.
        :param destination_directory: The root directory, into which the data will be copied.
        """
        super().__init__(destination_directory)
        self.dataset = dataset

    def get_dataset_download_url(self) -> str:
        if self.dataset is CvcMuscimaDataset.WriterIdentification:
            return "http://www.cvc.uab.es/cvcmuscima/CVCMUSCIMA_WI.zip"
        if self.dataset is CvcMuscimaDataset.StaffRemoval:
            return "http://www.cvc.uab.es/cvcmuscima/CVCMUSCIMA_SR.zip"

    def get_dataset_filename(self) -> str:
        if self.dataset is CvcMuscimaDataset.WriterIdentification:
            return "CVCMUSCIMA_WI.zip"
        if self.dataset is CvcMuscimaDataset.StaffRemoval:
            return "CVCMUSCIMA_SR.zip"

    def download_and_extract_dataset(self):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading CVC-MUSCIMA Dataset ({0})...".format(self.dataset))
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting CVC-MUSCIMA Dataset...")
        self.extract_dataset(self.destination_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/cvc_muscima",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = CvcMuscimaDatasetDownloader(flags.dataset_directory, CvcMuscimaDataset.StaffRemoval)
    dataset.download_and_extract_dataset()
