import os
import shutil
import unittest
from glob import glob

from omrdatasettools.downloaders.AudiverisOmrDatasetDownloader import AudiverisOmrDatasetDownloader
from omrdatasettools.image_generators.AudiverisOmrImageGenerator import AudiverisOmrImageGenerator


class AudiverisOmrImageGeneratorTest(unittest.TestCase):

    def test_download_extract_and_crop_bitmaps(self):
        # Arrange
        dataset_downloader = AudiverisOmrDatasetDownloader()

        # Act
        dataset_downloader.download_and_extract_dataset("temp/audiveris_omr_raw")
        image_generator = AudiverisOmrImageGenerator()
        image_generator.extract_symbols("temp/audiveris_omr_raw", "temp/audiveris_omr_img")
        all_image_files = [y for x in os.walk("temp/audiveris_omr_img") for y in glob(os.path.join(x[0], '*.png'))]
        actual_number_of_files = len(all_image_files)

        # Assert
        self.assertEqual(1056, actual_number_of_files)

        # Cleanup
        os.remove("AudiverisOmrDataset.zip")
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
