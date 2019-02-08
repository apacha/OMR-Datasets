import os
import shutil
import unittest
from glob import glob

from omrdatasettools.converters.MuscimaPlusPlusAnnotationConverter import MuscimaPlusPlusAnnotationConverter
from omrdatasettools.downloaders.MuscimaPlusPlusDatasetDownloader import MuscimaPlusPlusDatasetDownloader

from omrdatasettools.converters.EdiromAnnotationConverter import EdiromAnnotationConverter
from omrdatasettools.downloaders.EdiromDatasetDownloader import EdiromDatasetDownloader
from omrdatasettools.tests.DatasetDownloaderTest import DatasetDownloaderTest


class MuscimaPlusPlusAnnotationConverterTest(unittest.TestCase):
    def test_annotation_converter_expect_json_files_to_be_created(self):
        # Arrange
        expected_number_of_json_files = 140
        destination_directory = "MuscimaPlusPlus"
        downloader = MuscimaPlusPlusDatasetDownloader()
        annotation_zip_file = downloader.get_dataset_filename()
        imageset_zip_file = downloader.get_imageset_filename()
        downloader.download_and_extract_dataset(destination_directory)
        annotation_converter = MuscimaPlusPlusAnnotationConverter()

        # Act
        annotation_converter.convert_annotations_to_one_json_file_per_image(destination_directory)

        # Assert
        actual_number_of_json_files = len(glob(destination_directory + "/**/*.json", recursive=True))
        self.assertEqual(expected_number_of_json_files, actual_number_of_json_files)

        # Cleanup
        os.remove(annotation_zip_file)
        os.remove(imageset_zip_file)
        shutil.rmtree(destination_directory, ignore_errors=True)
