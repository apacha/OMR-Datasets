import argparse
import os

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class AudiverisOmrDatasetDownloader(DatasetDownloader):
    """ Loads and extracts the music symbols from the Audiveris OMR dataset.
        https://github.com/Audiveris/omr-dataset-tools
        Copyright 2017 by Hervé Bitteur under AGPL-3.0 license
    """

    def get_dataset_download_url(self) -> str:
        # In case, this URL does not work anymore, refer to the original repository
        # https://github.com/Audiveris/omr-dataset-tools/tree/master/data/input-images
        # for downloading the 8 files
        return "https://owncloud.tuwien.ac.at/index.php/s/lSkDZxtwBLs2FOK/download"

    def get_dataset_filename(self) -> str:
        return "AudiverisOmrDataset.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        """ Starts the download of the dataset and extracts it into the directory specified in the constructor """
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading Audiveris OMR dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting Audiveris OMR Dataset...")
        self.extract_dataset(os.path.abspath(destination_directory))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/audiveris_omr_raw",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset_downloader = AudiverisOmrDatasetDownloader()
    dataset_downloader.download_and_extract_dataset(flags.dataset_directory)
