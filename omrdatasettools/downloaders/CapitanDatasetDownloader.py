import argparse
import os

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class CapitanDatasetDownloader(DatasetDownloader):
    """ Downloads the Capitan dataset
        http://grfia.dlsi.ua.es/
        License unspecified, free for research purposes
    """

    def get_dataset_download_url(self) -> str:
        # Official URL: "http://grfia.dlsi.ua.es/cm/projects/timul/databases/BimodalHandwrittenSymbols.zip"
        return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/BimodalHandwrittenSymbols.zip"

    def get_dataset_filename(self) -> str:
        return "BimodalHandwrittenSymbols.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading Capitan Dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting Capitan Dataset...")
        self.extract_dataset(destination_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/capitan_raw",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset_downloader = CapitanDatasetDownloader()
    dataset_downloader.download_and_extract_dataset(flags.dataset_directory)
