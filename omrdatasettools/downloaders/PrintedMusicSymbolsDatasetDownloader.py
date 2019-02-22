import argparse
import os

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class PrintedMusicSymbolsDatasetDownloader(DatasetDownloader):
    """ Loads the Printed Music Symbols dataset
        https://github.com/apacha/PrintedMusicSymbolsDataset
        Copyright 2017 by Alexander Pacha under MIT license
     """

    def get_dataset_download_url(self) -> str:
        # If this link does not work anymore, find the images at https://github.com/apacha/PrintedMusicSymbolsDataset
        return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/PrintedMusicSymbolsDataset.zip"

    def get_dataset_filename(self) -> str:
        return "PrintedMusicSymbolsDataset.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading Printed Music Symbol dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting Printed Music Symbol dataset...")
        absolute_path_to_temp_folder = os.path.abspath('PrintedMusicSymbolsDataset')
        self.extract_dataset(absolute_path_to_temp_folder)

        DatasetDownloader.copytree(os.path.join(absolute_path_to_temp_folder, "PrintedMusicSymbolsDataset"),
                                   os.path.abspath(destination_directory))
        self.clean_up_temp_directory(absolute_path_to_temp_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/printed_images",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = PrintedMusicSymbolsDatasetDownloader()
    dataset.download_and_extract_dataset(flags.dataset_directory)
