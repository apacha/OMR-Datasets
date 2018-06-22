import os
import shutil
import unittest
from glob import glob

from omrdatasettools.downloaders.HomusDatasetDownloader import HomusDatasetDownloader
from omrdatasettools.image_generators.HomusImageGenerator import HomusImageGenerator


class HomusImageGeneratorTest(unittest.TestCase):
    def test_download_extract_and_draw_bitmaps(self):
        # Arrange
        datasetDownloader = HomusDatasetDownloader()

        # Act
        datasetDownloader.download_and_extract_dataset("temp/homus_raw")
        HomusImageGenerator.create_images("temp/homus_raw", "temp/homus_img", [3], 96, 192, 14)
        all_image_files = [y for x in os.walk("temp/homus_img") for y in glob(os.path.join(x[0], '*.png'))]
        actual_number_of_files = len(all_image_files)

        # Assert
        self.assertEqual(15200, actual_number_of_files)

        # Cleanup
        os.remove("HOMUS-2.0.zip")
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
