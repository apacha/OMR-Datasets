import os
import shutil
import unittest
from glob import glob

from omrdatasettools.AudiverisOmrImageGenerator import AudiverisOmrImageGenerator
from omrdatasettools.Downloader import Downloader
from omrdatasettools.OmrDataset import OmrDataset


class AudiverisOmrImageGeneratorTest(unittest.TestCase):

    def test_download_extract_and_crop_bitmaps(self):
        # Arrange
        dataset_downloader = Downloader()

        # Act
        dataset_downloader.download_and_extract_dataset(OmrDataset.Audiveris, "temp/audiveris_omr_raw")
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
