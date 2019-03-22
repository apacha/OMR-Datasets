import json
import os
import random
import shutil
from typing import List

import numpy

from omrdatasettools.downloaders.MuscimaPlusPlusDatasetDownloader import MuscimaPlusPlusDatasetDownloader


class MuscimaPlusPlusDatasetSplitter:
    """ Class for splitting the measure annotations from the MUSCIMA++ dataset into a reproducible
        training, validation and test set. """

    def __init__(self,
                 source_directory: str):
        """
        :param source_directory: The root directory, where the MUSCIMA++ dataset currently resides. If the dataset
                                 can not be found, it will automatically be downloaded into this directory
        """
        self.source_directory = source_directory
        self.destination_directory = os.path.join(source_directory, "v1.0", "data", "coco")

    def split_images_into_training_validation_and_test_set(self):
        path_to_json_annotations = os.path.join(self.source_directory, "v1.0", "data", "coco",
                                                "all_measure_annotations.json")
        training_json_annotations = os.path.join(self.source_directory, "v1.0", "data", "coco",
                                                 "training_measure_annotations.json")
        validation_json_annotations = os.path.join(self.source_directory, "v1.0", "data", "coco",
                                                   "validation_measure_annotations.json")
        testing_json_annotations = os.path.join(self.source_directory, "v1.0", "data", "coco",
                                                "testing_measure_annotations.json")
        if not os.path.exists(path_to_json_annotations):
            print(f"Could not find MUSCIMA++ dataset in {self.source_directory}. Downloading it automatically...")
            dataset_downloader = MuscimaPlusPlusDatasetDownloader()
            dataset_downloader.download_and_extract_dataset(self.source_directory)
            dataset_downloader.download_and_extract_measure_annotations(self.source_directory)

        print("Splitting data into training, validation and test sets...")

        with open(os.path.join(self.source_directory, "v1.0", "specifications", "testset-dependent.txt"), "r") as file:
            test_file_names = [line.replace('\n', '.png') for line in file.readlines()]

        all_file_names = os.listdir(os.path.join(self.source_directory, "v1.0", "data", "images"))
        training_validation_file_names = set(all_file_names) - set(test_file_names)
        validation_file_names = random.sample(training_validation_file_names, 20)
        training_file_names = training_validation_file_names - set(validation_file_names)

        with open(path_to_json_annotations, "r") as file:
            all_annotations = json.load(file)
        training_images = []
        training_image_ids = []
        training_annotations = []
        validation_images = []
        validation_image_ids = []
        validation_annotations = []
        testing_images = []
        testing_image_ids = []
        testing_annotations = []
        for image in all_annotations["images"]:
            if image["file_name"] in training_file_names:
                training_images.append(image)
                training_image_ids.append(image["id"])
            if image["file_name"] in validation_file_names:
                validation_images.append(image)
                validation_image_ids.append(image["id"])
            if image["file_name"] in test_file_names:
                testing_images.append(image)
                testing_image_ids.append(image["id"])

        for annotation in all_annotations["annotations"]:
            if annotation["image_id"] in training_image_ids:
                training_annotations.append(annotation)
            if annotation["image_id"] in validation_image_ids:
                validation_annotations.append(annotation)
            if annotation["image_id"] in testing_image_ids:
                testing_annotations.append(annotation)

        all_annotations["images"] = training_images
        all_annotations["annotations"] = training_annotations
        with open(training_json_annotations, "w") as file:
            json.dump(all_annotations, file, indent=4)

        all_annotations["images"] = validation_images
        all_annotations["annotations"] = validation_annotations
        with open(validation_json_annotations, "w") as file:
            json.dump(all_annotations, file, indent=4)

        all_annotations["images"] = testing_images
        all_annotations["annotations"] = testing_annotations
        with open(testing_json_annotations, "w") as file:
            json.dump(all_annotations, file, indent=4)


if __name__ == "__main__":
    dataset_splitter = MuscimaPlusPlusDatasetSplitter("../data/muscima_pp")
    dataset_splitter.split_images_into_training_validation_and_test_set()
