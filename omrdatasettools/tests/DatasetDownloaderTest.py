import os
import shutil
import unittest
from glob import glob

from omrdatasettools.downloaders import DatasetDownloader
from omrdatasettools.downloaders.AudiverisOmrDatasetDownloader import AudiverisOmrDatasetDownloader
from omrdatasettools.downloaders.CapitanDatasetDownloader import CapitanDatasetDownloader
from omrdatasettools.downloaders.CvcMuscimaDatasetDownloader import CvcMuscimaDatasetDownloader, CvcMuscimaDataset
from omrdatasettools.downloaders.FornesMusicSymbolsDatasetDownloader import FornesMusicSymbolsDatasetDownloader
from omrdatasettools.downloaders.HomusDatasetDownloader import HomusDatasetDownloader
from omrdatasettools.downloaders.MuscimaPlusPlusDatasetDownloader import MuscimaPlusPlusDatasetDownloader
from omrdatasettools.downloaders.OpenOmrDatasetDownloader import OpenOmrDatasetDownloader
from omrdatasettools.downloaders.PrintedMusicSymbolsDatasetDownloader import PrintedMusicSymbolsDatasetDownloader
from omrdatasettools.downloaders.RebeloMusicSymbolDataset1Downloader import RebeloMusicSymbolDataset1Downloader
from omrdatasettools.downloaders.RebeloMusicSymbolDataset2Downloader import RebeloMusicSymbolDataset2Downloader


class DatasetDownloaderTest(unittest.TestCase):
    def test_download_and_extract_audiveris_symbols_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "AudiverisRawData"
        downloader = AudiverisOmrDatasetDownloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 4
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_capitan_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "CapitanRawData"
        downloader = CapitanDatasetDownloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 1
        target_file_extension = "data"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_cvc_muscima_WI_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "CvcMuscimaWriterIdentificationData"
        downloader = CvcMuscimaDatasetDownloader(destination_directory, CvcMuscimaDataset.WriterIdentification)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 1
        target_file_extension = "png"

        # self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
        #                                                     target_file_extension, zip_file,
        #                                                     downloader)

    def test_download_and_extract_cvc_muscima_SR_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "CvcMuscimaStaffRemovalData"
        downloader = CvcMuscimaDatasetDownloader(destination_directory, CvcMuscimaDataset.StaffRemoval)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 1
        target_file_extension = "data"

        # self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
        #                                                     target_file_extension, zip_file,
        #                                                     downloader)

    def test_download_and_extract_fornes_symbols_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "FornesMusicSymbols"
        downloader = FornesMusicSymbolsDatasetDownloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 4094
        target_file_extension = "*.bmp"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_homus_v1_dataset_expect_folder_to_be_created(self):
        destination_directory = "HOMUS"
        downloader = HomusDatasetDownloader(".", version=1)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 15200
        target_file_extension = "*.txt"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_homus_v2_dataset_expect_folder_to_be_created(self):
        destination_directory = "HOMUS"
        downloader = HomusDatasetDownloader(".", version=2)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 15200
        target_file_extension = "*.txt"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_muscima_pp_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "MuscimaPlusPlus"
        downloader = MuscimaPlusPlusDatasetDownloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_with_staff_lines = 140
        number_of_samples_without_staff_lines = 140
        extra_files = 1
        number_of_xml_files_in_the_dataset = number_of_samples_with_staff_lines + number_of_samples_without_staff_lines + extra_files
        target_file_extension = "*.xml"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_xml_files_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_openomr_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "OpenOMR"
        downloader = OpenOmrDatasetDownloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 706
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_printed_symbols_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "PrintedMusicSymbols"
        downloader = PrintedMusicSymbolsDatasetDownloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 213
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_rebelo1_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "Rebelo1Images"
        downloader = RebeloMusicSymbolDataset1Downloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 7940
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def test_download_and_extract_rebelo2_dataset_expect_folder_to_be_created(self):
        # Arrange
        destination_directory = "Rebelo2Images"
        downloader = RebeloMusicSymbolDataset2Downloader(destination_directory)
        zip_file = downloader.get_dataset_filename()
        number_of_samples_in_the_dataset = 7307
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, zip_file,
                                                            downloader)

    def download_dataset_and_verify_correct_extraction(self, destination_directory: str,
                                                       number_of_samples_in_the_dataset: int,
                                                       target_file_extension: str, zip_file: str,
                                                       dataset_downloader: DatasetDownloader):
        # Arrange and Cleanup
        if os.path.exists(zip_file):
            os.remove(zip_file)
        shutil.rmtree(destination_directory, ignore_errors=True)

        # Act
        dataset_downloader.download_and_extract_dataset()

        # Assert
        all_files = [y for x in os.walk(destination_directory) for y in glob(os.path.join(x[0], target_file_extension))]
        actual_number_of_files = len(all_files)
        self.assertEqual(number_of_samples_in_the_dataset, actual_number_of_files)
        self.assertTrue(os.path.exists(zip_file))

        # Cleanup
        os.remove(zip_file)
        shutil.rmtree(destination_directory, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
