import argparse
import os
from enum import Enum
from glob import glob
from typing import List, Tuple

import numpy
from PIL import Image
from mung.io import read_nodes_from_file, parse_node_classes
from mung.node import Node
from tqdm import tqdm


class MaskType(Enum):
    """ The type of masks that should be generated """

    #: creates mask images, where each type of node gets the same color mask (for semantic segmentation).
    #: The classes staffLine, staff and staffSpace are ignored.
    NODES_SEMANTIC_SEGMENTATION = 1

    #: creates mask images, where the masks of the staff lines are contained for instance segmentation.
    #: All five lines that form a staff will have the same color.
    STAFF_LINES_INSTANCE_SEGMENTATION = 2

    #: creates mask images, where each staff will receive one big blob (filling the staff space regions) per staff
    #: line for instance segmentation. So each staff will have a different color.
    STAFF_BLOBS_INSTANCE_SEGMENTATION = 3


class MuscimaPlusPlusMaskImageGenerator:
    def __init__(self) -> None:
        self.path_of_this_file = os.path.dirname(os.path.realpath(__file__))
        self.class_to_color_mapping = dict()

    def render_node_masks(self, raw_data_directory: str, destination_directory: str, mask_type: MaskType):
        """
        Extracts all symbols from the raw XML documents and generates individual symbols from the masks

        :param raw_data_directory: The directory, that contains the xml-files and matching images
        :param destination_directory: The directory, in which the symbols should be generated into.
                                      Per file, one mask will be generated.
        :param mask_type: The type of masks that you want to generate, e.g., masks for each node or staff lines only.
        """
        print("Extracting Masks from Muscima++ Dataset...")

        node_classes = parse_node_classes(
            os.path.join(raw_data_directory, "v2.0", "specifications", "mff-muscima-mlclasses-annot.xml"))
        for index, node_class in enumerate(node_classes):
            self.class_to_color_mapping[node_class.name] = index + 1

        file_paths = self.__get_all_file_paths(raw_data_directory)
        for xml_file, png_file in tqdm(file_paths, desc="Generating mask images"):
            original_image = Image.open(png_file)  # type: Image.Image
            nodes = read_nodes_from_file(xml_file)
            destination_filename = os.path.basename(xml_file).replace(".xml", ".png")
            if mask_type == MaskType.NODES_SEMANTIC_SEGMENTATION:
                self.__render_masks_of_nodes_for_semantic_segmentation(nodes, destination_directory,
                                                                       destination_filename,
                                                                       original_image.width, original_image.height)
            if mask_type == MaskType.STAFF_LINES_INSTANCE_SEGMENTATION:
                self.__render_masks_of_staff_lines_for_instance_segmentation(nodes, destination_directory,
                                                                             destination_filename,
                                                                             original_image.width,
                                                                             original_image.height)
            if mask_type == MaskType.STAFF_BLOBS_INSTANCE_SEGMENTATION:
                self.__render_masks_of_staff_blob_for_instance_segmentation(nodes, destination_directory,
                                                                            destination_filename,
                                                                            original_image.width, original_image.height)
            original_image.close()

    def __get_all_file_paths(self, raw_data_directory: str) -> List[Tuple[str, str]]:
        """ Loads all XML-files that are located in the folder.
        :param raw_data_directory: Path to the raw directory, where the MUSCIMA++ dataset was extracted to
        """
        annotations_directory = os.path.join(raw_data_directory, "v2.0", "data", "annotations")
        xml_files = [y for x in os.walk(annotations_directory) for y in glob(os.path.join(x[0], '*.xml'))]
        images_directory = os.path.join(raw_data_directory, "v2.0", "data", "images")
        png_files = [y for x in os.walk(images_directory) for y in glob(os.path.join(x[0], '*.png'))]
        return list(zip(xml_files, png_files))

    def __render_masks_of_nodes_for_semantic_segmentation(self, nodes: List[Node], destination_directory: str,
                                                          destination_filename: str,
                                                          width: int, height: int):
        image = numpy.zeros((height, width), dtype=numpy.uint8)
        skipped_classes = ["staffSpace", "staff", "staffLine"]
        for node in reversed(nodes):
            if node.class_name in skipped_classes:
                continue
            try:
                symbol_class = node.class_name
                color_mask = node.mask * self.class_to_color_mapping[symbol_class]
                for i in range(node.height):
                    for j in range(node.width):
                        if color_mask[i, j] != 0:
                            image[node.top + i, node.left + j] = color_mask[i, j]
            except:
                print("Error drawing node {0}".format(node.unique_id))

        image = Image.fromarray(image, mode="L")
        os.makedirs(destination_directory, exist_ok=True)
        image.save(os.path.join(destination_directory, destination_filename))

    def __render_masks_of_staff_lines_for_instance_segmentation(self, nodes: List[Node], destination_directory: str,
                                                                destination_filename: str,
                                                                width: int, height: int):
        image = numpy.zeros((height, width), dtype=numpy.uint8)
        included_classes = ["staffLine"]
        staff_line_index = 0
        staff_index = 1
        for node in nodes:
            if node.class_name not in included_classes:
                continue
            if staff_line_index == 5:
                staff_line_index = 0
                staff_index += 1
            staff_line_index += 1
            try:
                color_mask = node.mask * staff_index
                for i in range(node.height):
                    for j in range(node.width):
                        if color_mask[i, j] != 0:
                            image[node.top + i, node.left + j] = color_mask[i, j]
            except:
                print("Error drawing node {0}".format(node.unique_id))

        image = Image.fromarray(image, mode="L")
        os.makedirs(destination_directory, exist_ok=True)
        image.save(os.path.join(destination_directory, destination_filename))

    def __render_masks_of_staff_blob_for_instance_segmentation(self, nodes: List[Node], destination_directory: str,
                                                               destination_filename: str,
                                                               width: int, height: int):
        image = numpy.zeros((height, width), dtype=numpy.uint8)
        included_classes = ["staffLine"]
        staff_line_index = 0
        staff_index = 1
        for node in nodes:
            if node.class_name not in included_classes:
                continue

            if staff_line_index == 4:
                try:
                    for i in range(first_staff_line_of_staff.top, node.bottom):
                        for j in range(node.left, node.right):
                            image[i, j] = staff_index
                except:
                    print("Error drawing node {0}".format(node.unique_id))

            if staff_line_index == 5:
                staff_index += 1
                staff_line_index = 0

            staff_line_index += 1
            if staff_line_index == 1:
                first_staff_line_of_staff = node

        image = Image.fromarray(image, mode="L")
        os.makedirs(destination_directory, exist_ok=True)
        image.save(os.path.join(destination_directory, destination_filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/muscima_pp",
        help="The directory, where the raw Muscima++ dataset can be found")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/muscima_pp_masks",
        help="The directory, where the generated bitmaps will be created")
    parser.add_argument(
        "--mask_type",
        type=str,
        default="nodes_semantic",
        help="One of the following types to be generated: [nodes_semantic, staff_lines, staff_blob]. Depending on the selected type, different"
             "mask images will be created: "
             "- nodes_semantic, creates mask images, where each type of node gets the same color mask (for semantic segmentation). The"
             "classes staffLine, staff and staffSpace are ignored"
             "- staff_lines, creates mask images, where the masks of the staff lines are contained for instance segmentation. All five "
             "lines that form a staff will have the same color."
             "- staff_blob, creates mask images, where each staff will receive one big blob (filling the staff space regions) per staff"
             "line for instance segmentation. So each staff will have a different color.")

    flags, unparsed = parser.parse_known_args()

    if flags.mask_type not in ["nodes_semantic", "staff_lines", "staff_blob"]:
        raise Exception(
            "Invalid option for mask type selected. Must be one of [nodes_semantic, staff_lines, staff_blob], but was " + flags.mask_type)

    if flags.mask_type == "nodes_semantic":
        mask_type = MaskType.NODES_SEMANTIC_SEGMENTATION
    if flags.mask_type == "staff_lines":
        mask_type = MaskType.STAFF_LINES_INSTANCE_SEGMENTATION
    if flags.mask_type == "staff_blob":
        mask_type = MaskType.STAFF_BLOBS_INSTANCE_SEGMENTATION

    mask_image_generator = MuscimaPlusPlusMaskImageGenerator()
    # noinspection PyUnboundLocalVariable
    mask_image_generator.render_node_masks(flags.raw_dataset_directory,
                                           flags.image_dataset_directory,
                                           mask_type)
