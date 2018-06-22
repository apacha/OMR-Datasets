import argparse
import os

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class HomusDatasetDownloader(DatasetDownloader):
    """ Downloads the HOMUS dataset
        http://grfia.dlsi.ua.es/homus/
        License unspecified
    """

    def __init__(self, version: int = 2):
        """
        Create and initializes a new dataset.
        :param version: Version of the HOMUS dataset, can either be 1 (official, original) or 2 (version with bug-fixes)
        """
        self.version = version

    def get_dataset_download_url(self) -> str:
        if self.version == 1:
            # Version 1.0 - official version
            return "http://grfia.dlsi.ua.es/homus/HOMUS.zip"
        elif self.version == 2:
            # Version 2.0 - version with bug-fixes, see https://github.com/apacha/Homus
            # If this link does not work anymore, you can find all files in the above mentioned git repo
            return "https://owncloud.tuwien.ac.at/index.php/s/5qVjo9HGGN1bN4I/download"
        else:
            raise Exception("Invalid version specified. Valid values are [1, 2]")

    def get_dataset_filename(self) -> str:
        if self.version == 1:
            return "HOMUS.zip"
        if self.version == 2:
            return "HOMUS-2.0.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading HOMUS Dataset (Version {0})...".format(self.version))
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting HOMUS Dataset...")
        self.extract_dataset(os.path.abspath(destination_directory))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/homus_raw",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = HomusDatasetDownloader(2)
    dataset.download_and_extract_dataset(flags.dataset_directory)
