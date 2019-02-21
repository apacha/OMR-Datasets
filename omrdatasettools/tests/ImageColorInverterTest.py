import os
import shutil
import unittest
from glob import glob

from omrdatasettools.converters.ImageColorInverter import ImageColorInverter
from omrdatasettools.downloaders.FornesMusicSymbolsDatasetDownloader import FornesMusicSymbolsDatasetDownloader


class ImageColorInverterTest(unittest.TestCase):
    def test_download_extract_and_invert_bitmaps(self):
        # Arrange
        temp_path = "temp/fornes_raw"
        datasetDownloader = FornesMusicSymbolsDatasetDownloader()
        datasetDownloader.download_and_extract_dataset(temp_path)

        # Act
        imageInverter = ImageColorInverter()
        imageInverter.invert_images(temp_path, "*.bmp")
        all_image_files = [y for x in os.walk(temp_path) for y in glob(os.path.join(x[0], '*.png'))]
        actual_number_of_files = len(all_image_files)

        # Assert
        self.assertEqual(4094, actual_number_of_files)

        # Cleanup
        os.remove("Music_Symbols.zip")
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
