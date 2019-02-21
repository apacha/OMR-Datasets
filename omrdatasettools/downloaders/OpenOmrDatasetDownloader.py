import argparse
import os
from distutils import dir_util
from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class OpenOmrDatasetDownloader(DatasetDownloader):
    """ Loads the OpenOMR Symbols dataset
        https://sourceforge.net/projects/openomr/
        Copyright 2013 by Arnaud F. Desaedeleer under GPL license
    """

    def get_dataset_download_url(self) -> str:
        # If this link does not work anymore, you can download the tar-ball from
        # https://sourceforge.net/projects/openomr/
        # and you will find the images in OpenOMR/neuralnetwork/ + train/validation/test folders
        return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/OpenOMR-Dataset.zip"

    def get_dataset_filename(self) -> str:
        return "OpenOMR-Dataset.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading OpenOMR dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting OpenOMR dataset...")
        absolute_path_to_temp_folder = os.path.abspath('OpenOmrDataset')
        self.extract_dataset(absolute_path_to_temp_folder)

        dir_util.copy_tree(os.path.join(absolute_path_to_temp_folder, "OpenOMR-Dataset"),
                           os.path.abspath(destination_directory))
        self.clean_up_temp_directory(absolute_path_to_temp_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/open_omr_raw",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = OpenOmrDatasetDownloader()
    dataset.download_and_extract_dataset(flags.dataset_directory)
