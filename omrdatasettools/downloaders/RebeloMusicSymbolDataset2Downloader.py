import argparse
import os

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class RebeloMusicSymbolDataset2Downloader(DatasetDownloader):
    """ Loads the Rebelo-2 dataset with music symbols
        http://www.inescporto.pt/~arebelo/index.php
        Copyright 2017 by Ana Rebelo under CC BY-SA 4.0 license
    """

    def get_dataset_download_url(self) -> str:
        return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/Rebelo-Music-Symbol-Dataset2.zip"

    def get_dataset_filename(self) -> str:
        return "Rebelo-Music-Symbol-Dataset2.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading Rebelo Symbol Dataset 2...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting Rebelo Symbol Dataset 2...")
        absolute_path_to_temp_folder = os.path.abspath('Rebelo-Music-Symbol-Dataset2')
        self.extract_dataset(absolute_path_to_temp_folder)

        DatasetDownloader.copytree(os.path.join(absolute_path_to_temp_folder, "database2"),
                                   os.path.abspath(destination_directory))
        self.clean_up_temp_directory(absolute_path_to_temp_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/rebelo2_images",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = RebeloMusicSymbolDataset2Downloader()
    dataset.download_and_extract_dataset(flags.dataset_directory)
