import argparse
import os

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class MuscimaPlusPlusDatasetDownloader(DatasetDownloader):
    """ Downloads the Muscima++ dataset
        https://ufal.mff.cuni.cz/muscima
        Copyright 2017 Jan Hajic jr. under CC-BY-NC-SA 4.0 license
    """

    def __init__(self, destination_directory: str):
        """
        Create and initializes a new dataset.
        :param destination_directory: The root directory, into which the data will be copied.
        """
        super().__init__(destination_directory)

    def get_dataset_download_url(self) -> str:
        return "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11372/LRT-2372/MUSCIMA-pp_v1.0.zip?sequence=1&isAllowed=y"

    def get_dataset_filename(self) -> str:
        return "MUSCIMA-pp_v1.0.zip"

    def download_and_extract_dataset(self):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading MUSCIMA++ Dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting MUSCIMA++ Dataset...")
        self.extract_dataset(self.destination_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/muscima_pp_raw",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = MuscimaPlusPlusDatasetDownloader(flags.dataset_directory)
    dataset.download_and_extract_dataset()
