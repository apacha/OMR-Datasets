import unittest
import os

from omrdatasettools.converters.csv_to_crop_object_conversion import convert_csv_annotations_to_cropobject

dir_path = os.path.dirname(os.path.realpath(__file__))


class CsvToCropObjectConversionTest(unittest.TestCase):
    def test_conversion_expect_number_of_objects(self):
        expected_number_of_crop_objects = 200
        crop_objects = convert_csv_annotations_to_cropobject(
            os.path.join(dir_path, "testdata", "CVC-MUSCIMA_W-01_N-10_D-ideal_1_detection.csv"),
            os.path.join(dir_path, "testdata", "CVC-MUSCIMA_W-01_N-10_D-ideal_1.png"))

        self.assertEqual(len(crop_objects), expected_number_of_crop_objects)

    def test_first_item_contains_correct_values(self):
        # Arrange
        # First line: CVC-MUSCIMA_W-01_N-10_D-ideal_1.png,138.93,2286.36,185.20,2316.52,8th_flag,1.00

        # Act
        crop_objects = convert_csv_annotations_to_cropobject(
            os.path.join(dir_path, "testdata", "CVC-MUSCIMA_W-01_N-10_D-ideal_1_detection.csv"),
            os.path.join(dir_path, "testdata", "CVC-MUSCIMA_W-01_N-10_D-ideal_1.png"))

        # Assert
        first_crop_object = crop_objects[0]
        self.assertEqual(first_crop_object.top, 139)
        self.assertEqual(first_crop_object.left, 2286)
        self.assertEqual(first_crop_object.bottom, 185)
        self.assertEqual(first_crop_object.right, 2316)
        self.assertEqual(first_crop_object.clsname, "8th_flag")
        self.assertEqual(first_crop_object.doc, "CVC-MUSCIMA_W-01_N-10_D-ideal_1.png")


if __name__ == '__main__':
    unittest.main()
