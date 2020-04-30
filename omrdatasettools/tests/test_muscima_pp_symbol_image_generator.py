import os
import shutil
import unittest
from glob import glob

from omrdatasettools.Downloader import Downloader
from omrdatasettools.MuscimaPlusPlusSymbolImageGenerator import MuscimaPlusPlusSymbolImageGenerator
from omrdatasettools.OmrDataset import OmrDataset


class MuscimaPlusPlusSymbolImageGeneratorTest(unittest.TestCase):
    def test_download_extract_and_render_all_symbols(self):
        # Arrange
        datasetDownloader = Downloader()

        # Act
        datasetDownloader.download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_V2, "temp/muscima_pp")
        image_generator = MuscimaPlusPlusSymbolImageGenerator()
        image_generator.extract_and_render_all_symbol_masks("temp/muscima_pp", "temp/muscima_pp/symbols")
        all_image_files = [y for x in os.walk("temp/muscima_pp/symbols") for y in glob(os.path.join(x[0], '*.png'))]
        expected_number_of_symbols = 102914
        actual_number_of_symbols = len(all_image_files)

        # Assert
        self.assertEqual(expected_number_of_symbols, actual_number_of_symbols)

        # Cleanup
        os.remove(OmrDataset.MuscimaPlusPlus_V2.get_dataset_filename())
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
