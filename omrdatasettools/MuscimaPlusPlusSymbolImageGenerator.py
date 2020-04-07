import argparse
import os
from glob import glob
from typing import List

from PIL import Image
from muscima.cropobject import CropObject
from muscima.io import parse_cropobject_list
from tqdm import tqdm

from omrdatasettools.ExportPath import ExportPath


class MuscimaPlusPlusSymbolImageGenerator:
    def __init__(self) -> None:
        super().__init__()
        self.path_of_this_file = os.path.dirname(os.path.realpath(__file__))

    def extract_and_render_all_symbol_masks(self, raw_data_directory: str, destination_directory: str):
        """
        Extracts all symbols from the raw XML documents and generates individual symbols from the masks

        :param raw_data_directory: The directory, that contains the xml-files and matching images
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        """
        print("Extracting Symbols from Muscima++ Dataset...")

        xml_files = self.get_all_xml_file_paths(raw_data_directory)
        crop_objects = self.load_crop_objects_from_xml_files(xml_files)
        self.render_masks_of_crop_objects_into_image(crop_objects, destination_directory)

    def get_all_xml_file_paths(self, raw_data_directory: str) -> List[str]:
        """ Loads all XML-files that are located in the folder.
        :param raw_data_directory: Path to the raw directory, where the MUSCIMA++ dataset was extracted to
        """
        raw_data_directory = os.path.join(raw_data_directory, "v1.0", "data", "cropobjects_manual")
        xml_files = [y for x in os.walk(raw_data_directory) for y in glob(os.path.join(x[0], '*.xml'))]
        return xml_files

    def load_crop_objects_from_xml_file(self, xml_file: str) -> List[CropObject]:
        crop_objects = []
        crop_objects.extend(self.get_crop_objects_from_xml_file(xml_file))

        for crop_object in crop_objects:
            # Some classes have special characters in their class name that we have to remove
            crop_object.clsname = crop_object.clsname.replace('"', '').replace('/', '').replace('.', '')

        # print("Loaded {0} crop-objects from {1}".format(len(crop_objects), xml_file))
        return crop_objects

    def load_crop_objects_from_xml_files(self, xml_files: List[str]) -> List[CropObject]:
        crop_objects = []
        for xml_file in tqdm(xml_files, desc="Loading crop-objects from xml-files", smoothing=0.1):
            crop_objects.extend(self.get_crop_objects_from_xml_file(xml_file))

        for crop_object in crop_objects:
            # Some classes have special characters in their class name that we have to remove
            crop_object.clsname = crop_object.clsname.replace('"', '').replace('/', '').replace('.', '')

        print("Loaded {0} crop-objects".format(len(crop_objects)))
        return crop_objects

    def get_crop_objects_from_xml_file(self, xml_file: str) -> List[CropObject]:
        # e.g., xml_file = 'data/muscima_pp/v0.9/data/cropobjects/CVC-MUSCIMA_W-01_N-10_D-ideal.xml'
        crop_objects = parse_cropobject_list(xml_file)
        return crop_objects

    def render_masks_of_crop_objects_into_image(self, crop_objects: List[CropObject], destination_directory: str):
        for crop_object in tqdm(crop_objects, desc="Generating images from crop-object masks", smoothing=0.1):
            symbol_class = crop_object.clsname
            # Make a copy of the mask to not temper with the original data
            mask = crop_object.mask.copy()
            # We want to draw black symbols on white canvas. The mask encodes foreground pixels
            # that we are interested in with a 1 and background pixels with a 0 and stores those values in
            # an uint8 numpy array. To use Image.fromarray, we have to generate a greyscale mask, where
            # white pixels have the value 255 and black pixels have the value 0. To achieve this, we simply
            # subtract one from each uint, and by exploiting the underflow of the uint we get the following mapping:
            # 0 (background) => 255 (white) and 1 (foreground) => 0 (black) which is exactly what we wanted.
            mask -= 1
            image = Image.fromarray(mask, mode="L")

            target_directory = os.path.join(destination_directory, symbol_class)
            os.makedirs(target_directory, exist_ok=True)

            export_path = ExportPath(destination_directory, symbol_class, crop_object.uid)
            image.save(export_path.get_full_path())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/muscima_pp_raw",
        help="The directory, where the raw Muscima++ dataset can be found")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/muscima_pp",
        help="The directory, where the generated bitmaps will be created")

    flags, unparsed = parser.parse_known_args()

    muscima_pp_image_generator = MuscimaPlusPlusSymbolImageGenerator()
    muscima_pp_image_generator.extract_and_render_all_symbol_masks(flags.raw_dataset_directory,
                                                                   flags.image_dataset_directory)
