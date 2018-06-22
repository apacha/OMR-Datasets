import os
import shutil
import unittest
from glob import glob

from omrdatasettools.downloaders.CapitanDatasetDownloader import CapitanDatasetDownloader
from omrdatasettools.image_generators.CapitanImageGenerator import CapitanImageGenerator


class CapitanImageGeneratorTest(unittest.TestCase):
    def test_download_extract_and_draw_bitmaps(self):
        # Arrange
        dataset_downloader = CapitanDatasetDownloader()
        image_generator = CapitanImageGenerator()

        # Act
        dataset_downloader.download_and_extract_dataset("temp/capitan_raw")
        symbols = image_generator.load_capitan_symbols("temp/capitan_raw")
        image_generator.draw_capitan_stroke_images(symbols, "temp/capitan_stroke", [3])
        image_generator.draw_capitan_score_images(symbols, "temp/capitan_score")

        # Assert
        all_stroke_images = [y for x in os.walk("temp/capitan_stroke") for y in glob(os.path.join(x[0], '*.png'))]
        all_score_images = [y for x in os.walk("temp/capitan_score") for y in glob(os.path.join(x[0], '*.png'))]
        self.assertEqual(10230, len(all_stroke_images))
        self.assertEqual(10230, len(all_score_images))

        # Cleanup
        os.remove(dataset_downloader.get_dataset_filename())
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
