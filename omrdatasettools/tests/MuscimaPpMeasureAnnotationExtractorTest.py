import json
import unittest
from glob import glob

from omrdatasettools.converters.MuscimaPpMeasureAnnotationExtractor import MuscimaPpMeasureAnnotationExtractor
from omrdatasettools.downloaders.MuscimaPlusPlusDatasetDownloader import MuscimaPlusPlusDatasetDownloader


class MuscimaPlusPlusAnnotationConverterTest(unittest.TestCase):

    def __init__(self, method_name: str = ...) -> None:
        super().__init__(method_name)
        self.dataset_directory = "MuscimaPlusPlus"

    def test_annotation_converter_expect_json_files_to_be_created(self):
        # Arrange
        expected_number_of_json_files = 140
        downloader = MuscimaPlusPlusDatasetDownloader()
        downloader.download_and_extract_dataset(self.dataset_directory)
        annotation_converter = MuscimaPpMeasureAnnotationExtractor()

        # Act
        annotation_converter.convert_measure_annotations_to_one_json_file_per_image(self.dataset_directory)

        # Assert
        actual_number_of_json_files = len(glob(self.dataset_directory + "/**/CVC-MUSCIMA_*.json", recursive=True))
        self.assertEqual(expected_number_of_json_files, actual_number_of_json_files)

    @unittest.skip("A measure_separator is duplicated in the data, that does not exist in the image, which causes this test to fail")
    def test_annotation_w04n20_has_three_system_measures(self):
        expected_number_of_system_measures = 3
        data = self._load_json_annotations("CVC-MUSCIMA_W-04_N-20_D-ideal.json")
        self.assertEqual(expected_number_of_system_measures, len(data["system_measures"]))

    @unittest.skip("A measure_separator is duplicated in the data, that does not exist in the image, which causes this test to fail")
    def test_annotation_w04n20_has_twelve_staff_measures(self):
        expected_number_of_stave_measures = 12
        data = self._load_json_annotations("CVC-MUSCIMA_W-04_N-20_D-ideal.json")
        self.assertEqual(expected_number_of_stave_measures, len(data["stave_measures"]))

    def test_annotation_w04n20_has_eight_staves(self):
        expected_number_of_staves = 8
        data = self._load_json_annotations("CVC-MUSCIMA_W-04_N-20_D-ideal.json")
        self.assertEqual(expected_number_of_staves, len(data["staves"]))

    def test_annotation_w46n20_has_three_system_measures(self):
        expected_number_of_system_measures = 3
        data = self._load_json_annotations("CVC-MUSCIMA_W-46_N-20_D-ideal.json")
        self.assertEqual(expected_number_of_system_measures, len(data["system_measures"]))

    def test_annotation_w46n20_has_twelve_staff_measures(self):
        expected_number_of_stave_measures = 12
        data = self._load_json_annotations("CVC-MUSCIMA_W-46_N-20_D-ideal.json")
        self.assertEqual(expected_number_of_stave_measures, len(data["stave_measures"]))

    def test_annotation_w46n20_has_eight_staves(self):
        expected_number_of_staves = 9
        data = self._load_json_annotations("CVC-MUSCIMA_W-46_N-20_D-ideal.json")
        self.assertEqual(expected_number_of_staves, len(data["staves"]))

    def _load_json_annotations(self, json_file_name):
        json_file = glob(self.dataset_directory + "/**/" + json_file_name, recursive=True)[0]
        with open(json_file) as file:
            data = json.load(file)
        return data
