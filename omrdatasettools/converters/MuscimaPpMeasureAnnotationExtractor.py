import argparse
import itertools
import json
import os
from glob import glob
from typing import List, Tuple

from PIL import Image
from muscima.cropobject import CropObject
from muscima.io import parse_cropobject_list
from tqdm import tqdm


def is_valid_annotation(bounding_box_dictionary):
    left, right = bounding_box_dictionary["left"], bounding_box_dictionary["right"]
    top, bottom = bounding_box_dictionary["top"], bounding_box_dictionary["bottom"]
    if left <= 0 or right <= 0 or top <= 0 or bottom <= 0:
        return False
    if left >= right:
        return False
    if top >= bottom:
        return False
    return True


class MuscimaPpMeasureAnnotationExtractor:
    def convert_measure_annotations_to_one_json_file_per_image(self, dataset_directory: str):
        json_directory = os.path.join(dataset_directory, "v1.0", "data", "json")
        os.makedirs(json_directory, exist_ok=True)

        xml_files = glob(dataset_directory + "/v1.0/data/cropobjects_withstaff/*.xml")
        image_files = glob(dataset_directory + "/v1.0/data/images/*.png")

        for xml_file in tqdm(xml_files, desc="Loading annotations and converting them to simple json"):
            sample_base_name = os.path.splitext(os.path.basename(xml_file))[0]
            image_file = [f for f in image_files if f.endswith(sample_base_name + ".png")][0]
            json_file = os.path.join(json_directory, sample_base_name + ".json")

            crop_objects = self.load_crop_objects(xml_file)
            all_staves, non_empty_staves = self.filter_staves(crop_objects)
            stave_coordinates = self.convert_stave_annotations(all_staves)
            stave_measures_coordinates = self.convert_stave_measure_annotations(crop_objects, non_empty_staves)
            system_measure_coordinates = self.convert_system_measure_annotations(crop_objects)
            self.dump_converted_annotations_into_json_file(image_file, json_file, stave_coordinates,
                                                           stave_measures_coordinates, system_measure_coordinates)

    def dump_converted_annotations_into_json_file(self, image_file, json_file, stave_coordinates,
                                                  stave_measures_coordinates, system_measure_coordinates):
        with open(json_file, 'w') as file:
            image = Image.open(image_file)  # type: Image.Image
            json.dump({'width': image.width, 'height': image.height, 'system_measures': system_measure_coordinates,
                       'stave_measures': stave_measures_coordinates, 'staves': stave_coordinates}, file, indent=4)

    def filter_staves(self, crop_objects) -> Tuple[List[CropObject], List[CropObject]]:
        all_staves = [c for c in crop_objects if c.clsname in ['staff']]
        non_empty_staves = [stave for stave in all_staves if any(stave.inlinks)]
        return all_staves, non_empty_staves

    def load_crop_objects(self, xml_file):
        crop_objects = parse_cropobject_list(xml_file)
        for crop_object in crop_objects:
            # Some classes have special characters in their class name that we have to remove
            crop_object.clsname = crop_object.clsname.replace('"', '').replace('/', '').replace('.', '')
        return crop_objects

    def convert_system_measure_annotations(self, crop_objects):
        # Get all staffs that belong together to a system
        system_measure_coordinates = []
        systems = set()
        measure_separators = [c for c in crop_objects if c.clsname in ['measure_separator']]
        for measure_separator in measure_separators:
            outgoing_staffs = frozenset(
                [c for c in measure_separator.get_outlink_objects(crop_objects) if c.clsname == 'staff'])
            systems.add(outgoing_staffs)
        for system in systems:
            all_system_objects = set(
                itertools.chain.from_iterable([stave.get_inlink_objects(crop_objects) for stave in system]))
            top = min(stave.top for stave in system)
            bottom = max(stave.bottom for stave in system)
            # noinspection PyRedeclaration
            left = min(stave.left for stave in system)
            end_of_system = max(stave.right for stave in system)
            end_of_last_object_in_system = max(o.right for o in all_system_objects)

            first_stave = next(iter(system))
            splitting_measure_separators = self.get_measure_separators(crop_objects, first_stave)
            for measure_separator in splitting_measure_separators:
                right = measure_separator.left
                system_measure = {'left': left, 'top': top, 'right': right, 'bottom': bottom}
                if is_valid_annotation(system_measure):
                    system_measure_coordinates.append(system_measure)
                left = measure_separator.right

            system_is_missing_terminal_barline = left < end_of_last_object_in_system
            if system_is_missing_terminal_barline:
                right = end_of_system
                system_measure = {'left': left, 'top': top, 'right': right, 'bottom': bottom}
                if is_valid_annotation(system_measure):
                    system_measure_coordinates.append(system_measure)

        return system_measure_coordinates

    def convert_stave_measure_annotations(self, crop_objects, staves):
        # Split staffs into separate measures per stave
        stave_measures_coordinates = []
        for stave in staves:
            # Some staves apparently has incorrectly attached elements, but if it has less than five objects, we consider it empty
            stave_is_empty = len(stave.inlinks) < 5
            if stave_is_empty:
                continue

            splitting_measure_separators = self.get_measure_separators(crop_objects, stave)
            all_stave_objects = set(stave.get_inlink_objects(crop_objects))

            top = stave.top
            bottom = stave.bottom
            # noinspection PyRedeclaration
            left = stave.left
            end_of_stave = stave.right
            end_of_last_object_in_stave = max(o.right for o in all_stave_objects)

            for measure_separator in splitting_measure_separators:
                right = measure_separator.left
                stave_measure = {'left': left, 'top': top, 'right': right, 'bottom': bottom}
                if is_valid_annotation(stave_measure):
                    stave_measures_coordinates.append(stave_measure)
                left = measure_separator.right

            stave_is_missing_terminal_barline = left < end_of_last_object_in_stave
            if stave_is_missing_terminal_barline:
                right = end_of_stave
                stave_measure = {'left': left, 'top': top, 'right': right, 'bottom': bottom}
                if is_valid_annotation(stave_measure):
                    stave_measures_coordinates.append(stave_measure)
        return stave_measures_coordinates

    def get_measure_separators(self, crop_objects, first_stave):
        splitting_measure_separators = [c for c in first_stave.get_inlink_objects(crop_objects) if
                                        c.clsname == 'measure_separator']  # type: List[CropObject]
        # Sort measure_separators from left to right
        splitting_measure_separators = sorted(splitting_measure_separators, key=lambda x: x.left)
        return splitting_measure_separators

    def convert_stave_annotations(self, staves):
        stave_coordinates = []
        for stave in staves:
            stave = {'left': stave.left, 'top': stave.top, 'right': stave.right, 'bottom': stave.bottom}
            if is_valid_annotation(stave):
                stave_coordinates.append(stave)
        return stave_coordinates


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads converts the measure annotations from the '
                                                 'MUSCIMA++ dataset into simple json format')
    parser.add_argument("--dataset_directory", type=str, default="../data/muscima_pp",
                        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    annotation_converter = MuscimaPpMeasureAnnotationExtractor()
    annotation_converter.convert_measure_annotations_to_one_json_file_per_image(flags.dataset_directory)
