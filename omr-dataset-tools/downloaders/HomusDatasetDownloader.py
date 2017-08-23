import argparse
import os

from downloaders.DatasetDownloader import DatasetDownloader


class HomusDatasetDownloader(DatasetDownloader):
    """ Downloads the HOMUS dataset
        http://grfia.dlsi.ua.es/homus/
        License unspecified
    """

    def __init__(self, destination_directory: str, version: int = 2):
        """
        Create and initializes a new dataset.
        :param destination_directory: The root directory, into which the data will be copied.
        :param version: Version of the HOMUS dataset, can either be 1 (official, original) or 2 (version with bug-fixes)
        """
        super().__init__(destination_directory)
        self.version = version

    def get_dataset_download_url(self) -> str:
        if self.version == 1:
            # Version 1.0 - official version
            return "http://grfia.dlsi.ua.es/homus/HOMUS.zip"
        elif self.version == 2:
            # Version 2.0 - version with bug-fixes, see https://github.com/apacha/Homus
            return "https://owncloud.tuwien.ac.at/index.php/s/5qVjo9HGGN1bN4I/download"

    def get_dataset_filename(self) -> str:
        if self.version == 1:
            return "HOMUS.zip"
        if self.version == 2:
            return "HOMUS-2.0.zip"

    def download_and_extract_dataset(self):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading HOMUS Dataset (Version {0})...".format(self.version))
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting HOMUS Dataset...")
        self.extract_dataset(self.destination_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/homus_raw",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = HomusDatasetDownloader(flags.dataset_directory)
    dataset.download_and_extract_dataset()
