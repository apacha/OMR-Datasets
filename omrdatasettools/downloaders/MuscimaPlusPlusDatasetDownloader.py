import argparse
import os

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class MuscimaPlusPlusDatasetDownloader(DatasetDownloader):
    """ Downloads the Muscima++ dataset
        https://ufal.mff.cuni.cz/muscima
        Copyright 2017 Jan Hajic jr. under CC-BY-NC-SA 4.0 license
    """

    def __init__(self, version: int = 1):
        """
        Create and initializes a new dataset.
        :param version: Version of the MUSCIMA++ dataset, can either be 1 (original by Jan Hajic) or 2 (adapted to
                        MuNG by Alexander Pacha).
        """
        self.version = version

    def get_dataset_download_url(self) -> str:
        # Official URL: "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11372/LRT-2372/MUSCIMA-pp_v1.0.zip?sequence=1&isAllowed=y"
        if self.version == 1:
            return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/MUSCIMA-pp_v1.0.zip"
        elif self.version == 2:
            return "https://github.com/OMR-Research/muscima-pp/releases/download/v2.0/MUSCIMA-pp_v2.0.zip"
        else:
            raise Exception("Invalid version specified. Valid values are [1, 2]")

    def get_dataset_filename(self) -> str:
        if self.version == 1:
            return "MUSCIMA-pp_v1.0.zip"
        if self.version == 2:
            return "MUSCIMA-pp_v2.0.zip"

    def get_images_download_url(self) -> str:
        # This URL contains the images of the CVC-MUSCIMA dataset, that were annotated in the MUSCIMA++ dataset
        return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/CVC_MUSCIMA_PP_Annotated-Images.zip"

    def get_imageset_filename(self) -> str:
        return "CVC_MUSCIMA_PP_Annotated-Images.zip"

    def get_measure_annotation_download_url(self):
        return "https://github.com/apacha/OMR-Datasets/releases/download/datasets/MUSCIMA-pp_v1.0-measure-annotations.zip"

    def get_measure_annotation_filename(self):
        return "MUSCIMA-pp_v1.0-measure-annotations.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        """
        Downloads and extracts the MUSCIMA++ dataset along with the images from the CVC-MUSCIMA dataset
        that were manually annotated (140 out of 1000 images).
        """
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
        DatasetDownloader.copytree(os.path.join(absolute_path_to_temp_folder, "fulls"),
                                   os.path.join(os.path.abspath(destination_directory), self.dataset_version(), "data",
                                                "images"))
        self.clean_up_temp_directory(absolute_path_to_temp_folder)

    def download_and_extract_measure_annotations(self, destination_directory: str):
        """
        Downloads the annotations only of stave-measures, system-measures and staves that were extracted
        from the MUSCIMA++ dataset via the :class:`omrdatasettools.converters.MuscimaPlusPlusAnnotationConverter`.

        The annotations from that extraction are provided in a simple json format with one annotation
        file per image and in the COCO format, where all annotations are stored in a single file.
        """
        if not os.path.exists(self.get_measure_annotation_filename()):
            print("Downloading MUSCIMA++ Measure Annotations...")
            self.download_file(self.get_measure_annotation_download_url(), self.get_measure_annotation_filename())

        print("Extracting MUSCIMA++ Annotations...")
        absolute_path_to_temp_folder = os.path.abspath('MuscimaPpMeasureAnnotations')
        self.extract_dataset(absolute_path_to_temp_folder, self.get_measure_annotation_filename())
        DatasetDownloader.copytree(os.path.join(absolute_path_to_temp_folder, "coco"),
                                   os.path.join(os.path.abspath(destination_directory), self.dataset_version(), "data",
                                                "coco"))
        DatasetDownloader.copytree(os.path.join(absolute_path_to_temp_folder, "json"),
                                   os.path.join(os.path.abspath(destination_directory), self.dataset_version(), "data",
                                                "json"))
        self.clean_up_temp_directory(absolute_path_to_temp_folder)

    def dataset_version(self):
        if self.version == 1:
            return "v1.0"
        if self.version == 2:
            return "v2.0"


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
    dataset.download_and_extract_measure_annotations(flags.dataset_directory)
