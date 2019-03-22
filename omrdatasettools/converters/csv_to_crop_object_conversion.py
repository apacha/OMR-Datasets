import argparse
import os
from glob import glob
from typing import List

import pandas as pd
from PIL import Image
from muscima.cropobject import CropObject
import numpy as np
from muscima.io import export_cropobject_list
from tqdm import tqdm


def convert_csv_annotations_to_cropobject(annotations_path: str, image_path: str) -> List[CropObject]:
    annotations = pd.read_csv(annotations_path)
    image = Image.open(image_path) # type: Image.Image

    crop_objects = []
    node_id = 0
    for index, annotation in annotations.iterrows():
        # Annotation example:
        # image_name,top,left,bottom,right,class_name,confidence
        # CVC-MUSCIMA_W-01_N-10_D-ideal_1.png,138.93,2286.36,185.20,2316.52,8th_flag,1.00
        image_name = annotation["image_name"]
        class_name = annotation["class_name"]
        top = round(annotation["top"])
        left = round(annotation["left"])
        width = round(annotation["right"] - annotation["left"])
        heigth = round(annotation["bottom"] - annotation["top"])
        crop_object = CropObject(node_id, class_name, top, left, width, heigth)
        crop_object.set_doc(image_name)
        crop_image = image.crop((left, top, crop_object.right, crop_object.bottom)).convert("1")
        # noinspection PyTypeChecker
        cropped_image_mask = np.array(crop_image)
        crop_object.set_mask(cropped_image_mask)
        crop_objects.append(crop_object)
        node_id += 1

    return crop_objects


def write_crop_objects_to_disk(crop_objects: List[CropObject], output_directory: str, output_filename: str) -> None:
    os.makedirs(output_directory, exist_ok=True)
    cropobject_xml_string = export_cropobject_list(crop_objects)
    with open(os.path.join(output_directory, output_filename), "w") as file:
        file.write(cropobject_xml_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads a dataset from the Edirom system')
    parser.add_argument('--annotations_directory', type=str, required=True,
                        help='Path to the annotation csv-files directory')
    parser.add_argument('--image_directory', type=str, required=True,
                        help='Path to the images from which the mask should be extracted')
    parser.add_argument("--output_directory", type=str, default="../converted_crop_objects",
                        help="The directory, where the converted CropObjects will be copied to")

    flags, unparsed = parser.parse_known_args()
    annotation_paths = glob(flags.annotations_directory + "/**/*.csv", recursive=True)
    image_paths = glob(flags.image_directory + "/**/*.png", recursive=True)
    for annotation_path, image_path in tqdm(zip(annotation_paths, image_paths), desc="Converting annotations", total=len(image_paths)):
        crop_objects = convert_csv_annotations_to_cropobject(annotation_path, image_path)
        output_filename = os.path.basename(image_path).replace('png', 'xml')
        write_crop_objects_to_disk(crop_objects, flags.output_directory, output_filename)
