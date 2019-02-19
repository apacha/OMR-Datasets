import argparse
import os
from distutils import dir_util

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class MuscimaPlusPlusDatasetDownloader(DatasetDownloader):
    """ Downloads the Muscima++ dataset
        https://ufal.mff.cuni.cz/muscima
        Copyright 2017 Jan Hajic jr. under CC-BY-NC-SA 4.0 license
    """

    def get_dataset_download_url(self) -> str:
        # Official URL: "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11372/LRT-2372/MUSCIMA-pp_v1.0.zip?sequence=1&isAllowed=y"
        return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/MUSCIMA-pp_v1.0.zip"

    def get_dataset_filename(self) -> str:
        return "MUSCIMA-pp_v1.0.zip"

    def get_images_download_url(self) -> str:
        # This URL contains the images of the CVC-MUSCIMA dataset, that were annotated in the MUSCIMA++ dataset
        return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/CVC_MUSCIMA_PP_Annotated-Images.zip"

    def get_imageset_filename(self) -> str:
        return "CVC_MUSCIMA_PP_Annotated-Images.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading MUSCIMA++ Dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        if not os.path.exists(self.get_imageset_filename()):
            print("Downloading MUSCIMA++ Images...")
            self.download_file(self.get_images_download_url(), self.get_imageset_filename())

        print("Extracting MUSCIMA++ Dataset...")
        self.extract_dataset(os.path.abspath(destination_directory))

        absolute_path_to_temp_folder = os.path.abspath('MuscimaPpImages')
        self.extract_dataset(absolute_path_to_temp_folder, self.get_imageset_filename())
        dir_util.copy_tree(os.path.join(absolute_path_to_temp_folder, "fulls"),
                           os.path.join(os.path.abspath(destination_directory), "v1.0", "data", "images"))
        self.clean_up_temp_directory(absolute_path_to_temp_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/muscima_pp",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = MuscimaPlusPlusDatasetDownloader()
    dataset.download_and_extract_dataset(flags.dataset_directory)
