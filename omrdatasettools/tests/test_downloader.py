import os
import shutil
import unittest
from glob import glob

from omrdatasettools.Downloader import Downloader
from omrdatasettools.OmrDataset import OmrDataset


class DownloaderTest(unittest.TestCase):

    def test_download_correct_url_resolution(self):
        downloader = OmrDataset.Audiveris
        url = downloader.get_dataset_download_url()
        expected_url = "https://github.com/apacha/OMR-Datasets/releases/download/datasets/AudiverisOmrDataset.zip"

        self.assertEqual(url, expected_url)

    def test_download_of_audiveris_dataset(self):
        destination_directory = "AudiverisRawData"
        dataset = OmrDataset.Audiveris
        number_of_samples_in_the_dataset = 4
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_capitan_dataset(self):
        destination_directory = "CapitanRawData"
        dataset = OmrDataset.Capitan
        number_of_samples_in_the_dataset = 1
        target_file_extension = "data"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_baro_dataset(self):
        destination_directory = "Baro"
        dataset = OmrDataset.Baro
        number_of_samples_in_the_dataset = 212
        target_file_extension = "*.txt"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    @unittest.skip("Only run, if you have time to kill")
    def test_download_of_cvc_muscima_writer_identification_dataset(self):
        destination_directory = "CvcMuscimaWriterIdentificationData"
        dataset = OmrDataset.CvcMuscima_WriterIdentification
        number_of_samples_in_the_dataset = 3000
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    @unittest.skip("Only run, if you have time to kill")
    def test_download_of_cvc_muscima_staff_removal_dataset(self):
        destination_directory = "CvcMuscimaStaffRemovalData"
        dataset = OmrDataset.CvcMuscima_StaffRemoval
        number_of_samples_in_the_dataset = 36000
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    @unittest.skip("Only run, if you have time to kill")
    def test_download_of_cvc_muscima_multi_conditional_aligned_dataset(self):
        destination_directory = "CvcMuscimaMultiConditionAlignedData"
        dataset = OmrDataset.CvcMuscima_MultiConditionAligned
        number_of_samples_in_the_dataset = 10000
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_fornes_dataset(self):
        destination_directory = "FornesMusicSymbols"
        dataset = OmrDataset.Fornes
        number_of_samples_in_the_dataset = 4094
        target_file_extension = "*.bmp"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_and_extract_bargheer_edirom_dataset_expect_folder_to_be_created(self):
        destination_directory = "Bargheer"
        dataset = OmrDataset.Edirom_Bargheer
        number_of_samples_in_the_dataset = 9
        target_file_extension = "*.xml"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_and_extract_freischuetz_edirom_dataset_expect_folder_to_be_created(self):
        destination_directory = "FreischuetzDigital"
        dataset = OmrDataset.Edirom_FreischuetzDigital
        number_of_samples_in_the_dataset = 15
        target_file_extension = "*.xml"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_homus_v1_dataset(self):
        destination_directory = "HOMUS"
        dataset = OmrDataset.Homus_V1
        number_of_samples_in_the_dataset = 15200
        target_file_extension = "*.txt"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_homus_v2_dataset(self):
        destination_directory = "HOMUS2"
        dataset = OmrDataset.Homus_V2
        number_of_samples_in_the_dataset = 15200
        target_file_extension = "*.txt"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_muscima_pp_v1_dataset(self):
        destination_directory = "MuscimaPlusPlus"
        dataset = OmrDataset.MuscimaPlusPlus_V1
        number_of_samples_with_staff_lines = 140
        number_of_samples_without_staff_lines = 140
        extra_files = 1
        number_of_xml_files_in_the_dataset = number_of_samples_with_staff_lines + number_of_samples_without_staff_lines + extra_files
        target_file_extension = "*.xml"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_xml_files_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_muscima_pp_v2_dataset(self):
        destination_directory = "MuscimaPlusPlus"
        dataset = OmrDataset.MuscimaPlusPlus_V2
        number_of_samples_with_staff_lines = 140
        extra_files = 1
        number_of_xml_files_in_the_dataset = number_of_samples_with_staff_lines + extra_files
        target_file_extension = "*.xml"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_xml_files_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_muscima_pp_v1_images(self):
        destination_directory = "MuscimaPlusPlus"
        dataset = OmrDataset.MuscimaPlusPlus_V1
        number_of_images = 140
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_images,
                                                            target_file_extension, dataset)

    def test_download_of_muscima_pp_v2_images(self):
        destination_directory = "MuscimaPlusPlus"
        dataset = OmrDataset.MuscimaPlusPlus_V2
        number_of_images = 140
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_images,
                                                            target_file_extension, dataset)

    def test_download_of_muscima_pp_measure_annotations(self):
        destination_directory = "MuscimaPlusPlus"
        dataset = OmrDataset.MuscimaPlusPlus_MeasureAnnotations
        number_of_annotation_files = 144
        target_file_extension = "*.json"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_annotation_files,
                                                            target_file_extension, dataset)

    def test_download_of_openomr_dataset(self):
        destination_directory = "OpenOMR"
        dataset = OmrDataset.OpenOmr
        number_of_samples_in_the_dataset = 706
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_printed_symbols_dataset(self):
        destination_directory = "PrintedMusicSymbols"
        dataset = OmrDataset.Printed
        number_of_samples_in_the_dataset = 213
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_rebelo1_dataset(self):
        destination_directory = "Rebelo1Images"
        dataset = OmrDataset.Rebelo1
        number_of_samples_in_the_dataset = 7940
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_rebelo2_dataset(self):
        destination_directory = "Rebelo2Images"
        dataset = OmrDataset.Rebelo2
        number_of_samples_in_the_dataset = 7307
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def test_download_of_deepscores_dataset(self):
        destination_directory = "DeepScoresV1Extended"
        dataset = OmrDataset.DeepScores_V1_Extended
        number_of_samples_in_the_dataset = 3408
        target_file_extension = "*.png"

        self.download_dataset_and_verify_correct_extraction(destination_directory, number_of_samples_in_the_dataset,
                                                            target_file_extension, dataset)

    def download_dataset_and_verify_correct_extraction(self: unittest.TestCase, destination_directory: str,
                                                       number_of_samples_in_the_dataset: int,
                                                       target_file_extension: str, dataset: OmrDataset):
        # Arrange and Cleanup
        if os.path.exists(dataset.get_dataset_filename()):
            os.remove(dataset.get_dataset_filename())
        shutil.rmtree(destination_directory, ignore_errors=True)
        downloader = Downloader()

        # Act
        downloader.download_and_extract_dataset(dataset, destination_directory)

        # Assert
        all_files = glob(destination_directory + "/**/" + target_file_extension, recursive=True)
        actual_number_of_files = len(all_files)
        self.assertEqual(number_of_samples_in_the_dataset, actual_number_of_files)
        self.assertTrue(os.path.exists(dataset.get_dataset_filename()))

        # Cleanup
        os.remove(dataset.get_dataset_filename())
        shutil.rmtree(destination_directory, ignore_errors=True)

        if __name__ == '__main__':
            unittest.main()
