import unittest

from omrdatasettools.ExportPath import ExportPath


class ExportPathTest(unittest.TestCase):
    def test_get_full_path_without_stroke_thickness(self):
        # Arrange
        export_path = ExportPath("data/images", "3-4-Time", "1-13", "png")

        # Act
        full_path = export_path.get_full_path()

        # Assert
        full_path = full_path.replace('\\', '/')
        self.assertEqual("data/images/3-4-Time/1-13.png", full_path)

    def test_get_full_path(self):
        # Arrange
        export_path = ExportPath("data/images", "3-4-Time", "1-13", "png", 3)

        # Act
        full_path = export_path.get_full_path()

        # Assert
        full_path = full_path.replace('\\', '/')
        self.assertEqual("data/images/3-4-Time/1-13_3.png", full_path)

    def test_get_full_path_with_offset(self):
        # Arrange
        export_path = ExportPath("data/images", "3-4-Time", "1-13", "png", 3)

        # Act
        full_path = export_path.get_full_path(33)

        # Assert
        full_path = full_path.replace('\\', '/')
        self.assertEqual("data/images/3-4-Time/1-13_3_offset_33.png", full_path)

    def test_get_class_name_and_file_path(self):
        # Arrange
        export_path = ExportPath("data/images", "3-4-Time", "1-13", "png", 3)

        # Act
        full_path = export_path.get_class_name_and_file_path()

        # Assert
        full_path = full_path.replace('\\', '/')
        self.assertEqual("3-4-Time/1-13_3.png", full_path)

    def test_get_class_name_and_file_path_with_offset(self):
        # Arrange
        export_path = ExportPath("data/images", "3-4-Time", "1-13", "png", 3)

        # Act
        full_path = export_path.get_class_name_and_file_path(33)

        # Assert
        full_path = full_path.replace('\\', '/')
        self.assertEqual("3-4-Time/1-13_3_offset_33.png", full_path)


if __name__ == '__main__':
    unittest.main()
