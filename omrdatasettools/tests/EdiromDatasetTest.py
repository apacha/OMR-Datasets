import unittest

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
