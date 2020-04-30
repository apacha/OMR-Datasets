import argparse
import os
from glob import glob
from typing import List

from PIL import Image
from mung.io import read_nodes_from_file
from mung.node import Node
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
        print("Extracting Symbols from MUSCIMA++ Dataset...")

        xml_files = self.get_all_xml_file_paths(raw_data_directory)
        crop_objects = self.load_nodes_from_xml_files(xml_files)
        self.render_masks_of_nodes_into_image(crop_objects, destination_directory)

    def get_all_xml_file_paths(self, raw_data_directory: str) -> List[str]:
        """ Loads all XML-files that are located in the folder.
        :param raw_data_directory: Path to the raw directory, where the MUSCIMA++ dataset was extracted to
        """
        raw_data_directory = os.path.join(raw_data_directory, "v2.0", "data", "annotations")
        xml_files = [y for x in os.walk(raw_data_directory) for y in glob(os.path.join(x[0], '*.xml'))]
        return xml_files

    def load_nodes_from_xml_files(self, xml_files: List[str]) -> List[Node]:
        nodes = []  # type: List[Node]
        for xml_file in tqdm(xml_files, desc="Loading nodes from xml-files", smoothing=0.1):
            nodes.extend(read_nodes_from_file(xml_file))

        print("Loaded {0} nodes".format(len(nodes)))
        return nodes

    def render_masks_of_nodes_into_image(self, nodes: List[Node], destination_directory: str):
        for node in tqdm(nodes, desc="Generating images from node masks", smoothing=0.1):  # type: Node
            symbol_class = node.class_name
            # Make a copy of the mask to not temper with the original data
            mask = node.mask.copy()
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

            export_path = ExportPath(destination_directory, symbol_class, node.unique_id)
            image.save(export_path.get_full_path())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/muscima_pp",
        help="The directory, where the Muscima++ dataset can be found. Must be at least version 2.0.")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/muscima_pp/symbols",
        help="The directory, where the generated bitmaps will be created")

    flags, unparsed = parser.parse_known_args()

    muscima_pp_image_generator = MuscimaPlusPlusSymbolImageGenerator()
    muscima_pp_image_generator.extract_and_render_all_symbol_masks(flags.raw_dataset_directory,
                                                                   flags.image_dataset_directory)
