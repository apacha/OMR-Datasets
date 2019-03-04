import argparse
import os

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class BaroDatasetDownloader(DatasetDownloader):
    """ Downloads the Baro Single Stave dataset
        http://www.cvc.uab.es/people/abaro/datasets.html
        Copyright 2019 Arnau Baró, Pau Riba, Jorge Calvo-Zaragoza, and Alicia Fornés under CC-BY-NC-SA 4.0 license
    """

    def get_dataset_download_url(self) -> str:
        # Official URL: "http://www.cvc.uab.es/people/abaro/datasets/MUSCIMA_ABARO.zip"
        return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/BaroMuscima.zip"

    def get_dataset_filename(self) -> str:
        return "BaroMuscima.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading Baro Single Stave Dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting Baro Single Stave Dataset...")
        self.extract_dataset(destination_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/baro",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset_downloader = BaroDatasetDownloader()
    dataset_downloader.download_and_extract_dataset(flags.dataset_directory)
