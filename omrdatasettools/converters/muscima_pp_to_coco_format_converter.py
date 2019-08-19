from datetime import datetime
import json
import os
import re
import fnmatch
from glob import glob

from PIL import Image
import numpy as np

# Script for converting the MUSCIMA++ dataset into the COCO format, used by popular object detectors
from mung.io import parse_node_classes, read_nodes_from_file
from typing import Dict, List, Tuple

from shapely.geometry import Polygon
from skimage import measure
from tqdm import tqdm

INFO = {
    "description": "MUSCIMA++ dataset",
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


def create_annotation_info(annotation_id, image_id, category_id, node):
    bounding_box = [node.left, node.top, node.width, node.height]
    segmentation = []

    annotation_info = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": category_id,
        "iscrowd": 0,
        "area": 0.0,
        "bbox": bounding_box,
        "segmentation": segmentation,
    }

    return annotation_info


def get_categories(node_classes_file_path) -> Tuple[List[Dict[str,str]],Dict[str,str]]:
    node_classes = parse_node_classes(node_classes_file_path)
    categories = []
    for node_class in node_classes:
        categories.append(
            {
                'id': node_class.class_id,
                'name': node_class.name,
                'supercategory': node_class.group_name.split("/")[0],
            }
        )

    class_to_id_mapping = {c.name : c.class_id for c in node_classes}
    return categories, class_to_id_mapping


if __name__ == "__main__":
    # TODO: Obtain from arguments
    ROOT_DIR = '../data/muscima_pp/v2.0'
    IMAGE_DIR = os.path.join(ROOT_DIR, "data", "images")
    ANNOTATION_DIR = os.path.join(ROOT_DIR, "data", "annotations")

    CATEGORIES, class_name_to_category_id_mapping = get_categories(os.path.join(ROOT_DIR, "specifications", "mff-muscima-mlclasses-annot.xml"))

    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }

    image_id = 1
    annotation_id = 1
    annotation_file_paths = glob(ANNOTATION_DIR + "/*.xml")

    for annotation_file_path in tqdm(annotation_file_paths, desc="Parsing annotations"):
        nodes = read_nodes_from_file(annotation_file_path)

        image_name = os.path.splitext(os.path.basename(annotation_file_path))[0] + ".png"
        image = Image.open(os.path.join(IMAGE_DIR, image_name)) # type: Image.Image
        image_info = create_image_info(image_id, image_name, (image.width, image.height))
        coco_output["images"].append(image_info)

        for node in nodes:
            annotation_info = create_annotation_info(annotation_id, image_id, class_name_to_category_id_mapping[node.class_name], node)
            coco_output["annotations"].append(annotation_info)
            annotation_id = annotation_id + 1

        image_id = image_id + 1

    os.makedirs("{}/data/coco".format(ROOT_DIR), exist_ok=True)
    with open('{}/data/coco/all_annotations.json'.format(ROOT_DIR), 'w') as output_json_file:
        json.dump(coco_output, output_json_file, indent=4)
