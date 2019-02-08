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
    def convert_annotations_to_one_json_file_per_image(self, dataset_directory: str):
        json_directory = os.path.join(dataset_directory, "v1.0", "data", "json")
        os.makedirs(json_directory, exist_ok=True)

        xml_files = glob(dataset_directory + "/v1.0/data/cropobjects_withstaff/*.xml")
        image_files = glob(dataset_directory + "/v1.0/data/images/*.png")

        for xml_file in tqdm(xml_files, desc="Loading annotations and converting them to simple json"):
            image_file = \
                [f for f in image_files if f.endswith(os.path.splitext(os.path.basename(xml_file))[0] + ".png")][0]
            json_file = os.path.join(json_directory, os.path.splitext(os.path.basename(xml_file))[0] + ".json")
            crop_objects = parse_cropobject_list(xml_file)

            for crop_object in crop_objects:
                # Some classes have special characters in their class name that we have to remove
                crop_object.clsname = crop_object.clsname.replace('"', '').replace('/', '').replace('.', '')

            staffs = [c for c in crop_objects if c.clsname in ['staff']]
            staff_coordinates = []
            for staff in staffs:
                staff_coordinates.append(
                    {'left': staff.left, 'top': staff.top, 'right': staff.right, 'bottom': staff.bottom})

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

            with open(json_file, 'w') as file:
                image = Image.open(image_file)  # type: Image.Image
                json.dump({'width': image.width, 'height': image.height, 'system_measures': system_measure_coordinates,
                           'stave_measures': staff_measures_coordinates, 'staves': staff_coordinates}, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads converts the MUSCIMA++ dataset into simple json format')
    parser.add_argument("--dataset_directory", type=str, default="../data/muscima_pp",
                        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    annotation_converter = MuscimaPlusPlusAnnotationConverter()
    annotation_converter.convert_annotations_to_one_json_file_per_image(flags.dataset_directory)
