import argparse
import os
from glob import glob

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class FornesMusicSymbolsDatasetDownloader(DatasetDownloader):
    """ Loads the Fornes Music Symbols dataset
        http://www.cvc.uab.es/~afornes/
        License unspecified - citation requested
        """

    def get_dataset_download_url(self) -> str:
        # Official URL: "http://www.cvc.uab.es/cvcmuscima/datasets/Music_Symbols.zip"
        return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/Music_Symbols.zip"

    def get_dataset_filename(self) -> str:
        return "Music_Symbols.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading Fornes Music Symbol dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting Fornes Music Symbol dataset...")
        absolute_path_to_temp_folder = os.path.abspath('Fornes-Music-Symbols')
        self.extract_dataset(absolute_path_to_temp_folder)

        self.__fix_capital_file_endings(absolute_path_to_temp_folder)

        DatasetDownloader.copytree(os.path.join(absolute_path_to_temp_folder, "Music_Symbols"),
                           os.path.abspath(destination_directory))
        self.clean_up_temp_directory(absolute_path_to_temp_folder)

    def __fix_capital_file_endings(self, absolute_path_to_temp_folder):
        image_with_capital_file_ending = [y for x in os.walk(absolute_path_to_temp_folder) for y in
                                          glob(os.path.join(x[0], "*.BMP"))]
        for image in image_with_capital_file_ending:
            os.rename(image, image[:-3] + "bmp")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/fornes_raw",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = FornesMusicSymbolsDatasetDownloader()
    dataset.download_and_extract_dataset(flags.dataset_directory)
