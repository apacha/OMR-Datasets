from datetime import datetime
import json
import os
import re
import fnmatch
from glob import glob

from PIL import Image
import numpy as np

# Script for converting measure annotations of the MUSCIMA++ dataset into the COCO format, used by popular object detectors

ROOT_DIR = '../data/muscima_pp/v1.0/data'
IMAGE_DIR = os.path.join(ROOT_DIR, "images")
ANNOTATION_DIR = os.path.join(ROOT_DIR, "json")

INFO = {
    "description": "MUSCIMA++ dataset for Measure Detection",
    "url": "https://apacha.github.io/OMR-Datasets/",
    "version": "0.1",
    "year": 2019,
    "contributor": "apacha",
    "date_created": datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/4.0/"
    }
]

SYSTEM_MEASURE_ID = 1
STAVE_MEASURE_ID = 2
STAVE_ID = 3

CATEGORIES = [
    {
        'id': SYSTEM_MEASURE_ID,
        'name': 'system_measure',
        'supercategory': 'region',
    },
    {
        'id': STAVE_MEASURE_ID,
        'name': 'stave_measure',
        'supercategory': 'region',
    },
    {
        'id': STAVE_ID,
        'name': 'stave',
        'supercategory': 'region',
    },
]


def coordinates_to_bounding_box(coordinates_dictionary):
    left = coordinates_dictionary['left']
    right = coordinates_dictionary['right']
    top = coordinates_dictionary['top']
    bottom = coordinates_dictionary['bottom']
    width = right - left
    height = bottom - top
    return [left, top, width, height]


def create_image_info(image_id, file_name, image_size,
                      date_captured=datetime.utcnow().isoformat(' '),
                      license_id=1, coco_url="", flickr_url=""):
    image_info = {
        "id": image_id,
        "file_name": file_name,
        "width": image_size[0],
        "height": image_size[1],
        "date_captured": date_captured,
        "license": license_id,
        "coco_url": coco_url,
        "flickr_url": flickr_url
    }

    return image_info


def create_annotation_info(annotation_id, image_id, category_id, bounding_box):
    annotation_info = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "iscrowd": 0,
        "area": 0.0,
        "bbox": bounding_box,
        "segmentation": [],
    }

    return annotation_info


def main():
    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }

    image_id = 1
    annotation_id = 1
    annotation_file_paths = glob(ANNOTATION_DIR + "/*.json")

    for annotation_file_path in annotation_file_paths:
        with open(annotation_file_path, 'r') as file:
            annotation = json.load(file)

        image_path = os.path.splitext(os.path.basename(annotation_file_path))[0] + ".png"
        image_info = create_image_info(image_id, image_path, (annotation["width"], annotation["height"]))
        coco_output["images"].append(image_info)

        system_measure_coordinates = annotation['system_measures']
        for system_measure in system_measure_coordinates:
            bounding_box = coordinates_to_bounding_box(system_measure)
            annotation_info = create_annotation_info(annotation_id, image_id, SYSTEM_MEASURE_ID, bounding_box)
            coco_output["annotations"].append(annotation_info)
            annotation_id = annotation_id + 1

        stave_measure_coordinates = annotation['stave_measures']
        for staff_measure in stave_measure_coordinates:
            bounding_box = coordinates_to_bounding_box(staff_measure)
            annotation_info = create_annotation_info(annotation_id, image_id, STAVE_MEASURE_ID, bounding_box)
            coco_output["annotations"].append(annotation_info)
            annotation_id = annotation_id + 1

        stave_coordinates = annotation['staves']
        for stave in stave_coordinates:
            bounding_box = coordinates_to_bounding_box(stave)
            annotation_info = create_annotation_info(annotation_id, image_id, STAVE_ID, bounding_box)
            coco_output["annotations"].append(annotation_info)
            annotation_id = annotation_id + 1

        image_id = image_id + 1

    with open('{}/measure_detection_muscimarker.json'.format(ROOT_DIR), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)


if __name__ == "__main__":
    main()
