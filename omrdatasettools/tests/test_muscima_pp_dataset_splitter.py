import shutil
import unittest
from glob import glob

from omrdatasettools.converters.MuscimaPlusPlusDatasetSplitter import MuscimaPlusPlusDatasetSplitter


class MuscimaPlusPlusDatasetSplitterTest(unittest.TestCase):

    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        self.dataset_directory = "MuscimaPlusPlus"

    def test_dataset_splitting_expect_json_files_to_be_created(self):
        # Arrange
        expected_number_of_json_files = 144
        dataset_splitter = MuscimaPlusPlusDatasetSplitter(self.dataset_directory)

        # Act
        dataset_splitter.split_images_into_training_validation_and_test_set()

        # Assert
        actual_number_of_json_files = len(glob(self.dataset_directory + "/**/*.json", recursive=True))
        self.assertEqual(expected_number_of_json_files, actual_number_of_json_files)

        # Cleanup
        shutil.rmtree(self.dataset_directory, ignore_errors=True)
