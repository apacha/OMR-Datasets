import os
import shutil
import unittest
from glob import glob

from omrdatasettools.converters.EdiromAnnotationConverter import EdiromAnnotationConverter
from omrdatasettools.downloaders.EdiromDatasetDownloader import EdiromDatasetDownloader
from omrdatasettools.tests.DatasetDownloaderTest import DatasetDownloaderTest


class EdiromDatasetTest(unittest.TestCase):
    def test_download_and_extract_bargheer_edirom_dataset_expect_folder_to_be_created(self):
        destination_directory = "Bargheer"
        downloader = EdiromDatasetDownloader("Bargheer")
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 9
        target_file_extension = "*.xml"

        # noinspection PyCallByClass
        DatasetDownloaderTest.download_dataset_and_verify_correct_extraction(self, destination_directory,
                                                                             number_of_samples_in_the_dataset,
                                                                             target_file_extension, zip_file,
                                                                             downloader)

    def test_download_and_extract_freischuetz_edirom_dataset_expect_folder_to_be_created(self):
        destination_directory = "FreischuetzDigital"
        downloader = EdiromDatasetDownloader("FreischuetzDigital")
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 15
        target_file_extension = "*.xml"

        # noinspection PyCallByClass
        DatasetDownloaderTest.download_dataset_and_verify_correct_extraction(self, destination_directory,
                                                                             number_of_samples_in_the_dataset,
                                                                             target_file_extension, zip_file,
                                                                             downloader)

    def test_annotation_converter_expect_json_files_to_be_created(self):
        # Arrange
        expected_number_of_json_files = 114
        dataset = "Bargheer"
        destination_directory = "Bargheer"
        downloader = EdiromDatasetDownloader("Bargheer")
        zip_file = downloader.get_dataset_filename()
        downloader.download_and_extract_dataset(destination_directory)

        # Act
        annotation_converter = EdiromAnnotationConverter()
        annotation_converter.convert_annotations_to_one_json_file_per_image(".", dataset)

        # Assert
        actual_number_of_json_files = len(glob(destination_directory + "/**/*.json", recursive=True))
        self.assertEqual(expected_number_of_json_files, actual_number_of_json_files)

        # Cleanup
        os.remove(zip_file)
        shutil.rmtree(destination_directory, ignore_errors=True)
