import argparse
import json
import os
from glob import glob
from typing import List

from PIL import Image
from muscima.cropobject import CropObject
from muscima.io import parse_cropobject_list
from tqdm import tqdm


class MuscimaPlusPlusAnnotationConverter:
    def convert_measure_annotations_to_one_json_file_per_image(self, dataset_directory: str):
        json_directory = os.path.join(dataset_directory, "v1.0", "data", "json")
        os.makedirs(json_directory, exist_ok=True)

        image_files, xml_files = self.get_image_and_annotation_file_paths(dataset_directory)

        for xml_file in tqdm(xml_files, desc="Loading annotations and converting them to simple json"):
            sample_base_name = os.path.splitext(os.path.basename(xml_file))[0]
            image_file = [f for f in image_files if f.endswith(sample_base_name + ".png")][0]
            json_file = os.path.join(json_directory, sample_base_name + ".json")

            crop_objects = self.load_crop_objects(xml_file)
            staffs = self.filter_staffs(crop_objects)
            staff_coordinates = self.convert_staff_annotations(staffs)
            staff_measures_coordinates = self.convert_staff_measure_annotations(crop_objects, staffs)
            system_measure_coordinates = self.convert_system_measure_annotations(crop_objects)
            self.dump_converted_annotations_into_json_file(image_file, json_file, staff_coordinates,
                                                           staff_measures_coordinates, system_measure_coordinates)

    def get_image_and_annotation_file_paths(self, dataset_directory):
        xml_files = glob(dataset_directory + "/v1.0/data/cropobjects_withstaff/*.xml")
        image_files = glob(dataset_directory + "/v1.0/data/images/*.png")
        return image_files, xml_files

    def dump_converted_annotations_into_json_file(self, image_file, json_file, staff_coordinates,
                                                  staff_measures_coordinates, system_measure_coordinates):
        with open(json_file, 'w') as file:
            image = Image.open(image_file)  # type: Image.Image
            json.dump({'width': image.width, 'height': image.height, 'system_measures': system_measure_coordinates,
                       'stave_measures': staff_measures_coordinates, 'staves': staff_coordinates}, file)

    def filter_staffs(self, crop_objects):
        staffs = [c for c in crop_objects if c.clsname in ['staff']]
        return staffs

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
            top = min(s.top for s in system)
            bottom = max(s.bottom for s in system)
            # noinspection PyRedeclaration
            left = min(s.left for s in system)
            first_stave = next(iter(system))
            splitting_measure_separators = [c for c in first_stave.get_inlink_objects(crop_objects) if
                                            c.clsname == 'measure_separator']  # type: List[CropObject]
            # Sort measure_separators from left to right
            splitting_measure_separators = sorted(splitting_measure_separators, key=lambda x: x.left)
            for measure_separator in splitting_measure_separators:
                right = measure_separator.left
                system_measure = {'left': left, 'top': top, 'right': right, 'bottom': bottom}
                system_measure_coordinates.append(system_measure)
                left = measure_separator.right
        return system_measure_coordinates

    def convert_staff_measure_annotations(self, crop_objects, staffs):
        # Split staffs into separate measures per staff
        staff_measures_coordinates = []
        for staff in staffs:
            splitting_measure_separators = [c for c in staff.get_inlink_objects(crop_objects) if
                                            c.clsname == 'measure_separator']  # type: List[CropObject]
            # Sort measure_separators from left to right
            splitting_measure_separators = sorted(splitting_measure_separators, key=lambda x: x.left)
            top = staff.top
            bottom = staff.bottom
            # noinspection PyRedeclaration
            left = staff.left
            for measure_separator in splitting_measure_separators:
                right = measure_separator.left
                staff_measure = {'left': left, 'top': top, 'right': right, 'bottom': bottom}
                staff_measures_coordinates.append(staff_measure)
                left = measure_separator.right
        return staff_measures_coordinates

    def convert_staff_annotations(self, staffs):
        staff_coordinates = []
        for staff in staffs:
            staff_coordinates.append(
                {'left': staff.left, 'top': staff.top, 'right': staff.right, 'bottom': staff.bottom})
        return staff_coordinates


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads converts the measure annotations from the '
                                                 'MUSCIMA++ dataset into simple json format')
    parser.add_argument("--dataset_directory", type=str, default="../data/muscima_pp",
                        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    annotation_converter = MuscimaPlusPlusAnnotationConverter()
    annotation_converter.convert_measure_annotations_to_one_json_file_per_image(flags.dataset_directory)
