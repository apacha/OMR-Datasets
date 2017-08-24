import argparse
import os
from distutils import dir_util

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class PrintedMusicSymbolsDatasetDownloader(DatasetDownloader):
    """ Loads the Printed Music Symbols dataset
        https://github.com/apacha/PrintedMusicSymbolsDataset
        Copyright 2017 by Alexander Pacha under MIT license
     """

    def __init__(self, destination_directory: str):
        """
        Create and initializes a new dataset.
        :param destination_directory: The root directory, into which the data will be copied.
        """
        super().__init__(destination_directory)

    def get_dataset_download_url(self) -> str:
        # If this link does not work anymore, find the images at https://github.com/apacha/PrintedMusicSymbolsDataset
        return "https://owncloud.tuwien.ac.at/index.php/s/qpIco99mCw2yGVK/download"

    def get_dataset_filename(self) -> str:
        return "PrintedMusicSymbolsDataset.zip"

    def download_and_extract_dataset(self):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading Printed Music Symbol dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting Printed Music Symbol dataset...")
        absolute_path_to_temp_folder = os.path.abspath('PrintedMusicSymbolsDataset')
        self.extract_dataset(absolute_path_to_temp_folder)

        os.makedirs(self.destination_directory, exist_ok=True)
        dir_util.copy_tree(os.path.join(absolute_path_to_temp_folder, "PrintedMusicSymbolsDataset"),
                           self.destination_directory)
        self.clean_up_temp_directory(absolute_path_to_temp_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/images",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = PrintedMusicSymbolsDatasetDownloader(flags.dataset_directory)
    dataset.download_and_extract_dataset()
