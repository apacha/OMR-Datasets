import os
import shutil
import unittest
from glob import glob

from omrdatasettools.downloaders.MuscimaPlusPlusDatasetDownloader import MuscimaPlusPlusDatasetDownloader
from omrdatasettools.image_generators.MuscimaPlusPlusMaskImageGenerator import \
    MuscimaPlusPlusMaskImageGenerator


class MuscimaPlusPlusMaskImageGeneratorTest(unittest.TestCase):
    @unittest.skip("Takes very long and is not very useful yet")
    def test_download_extract_and_render_all_symbols(self):
        # Arrange
        datasetDownloader = MuscimaPlusPlusDatasetDownloader(dataset_version="2.0")

        # Act
        datasetDownloader.download_and_extract_dataset("temp/muscima_pp_raw")
        image_generator = MuscimaPlusPlusMaskImageGenerator()
        image_generator.render_instance_segmentation_masks("temp/muscima_pp_raw", "temp/muscima_img")
        all_image_files = [y for x in os.walk("temp/muscima_img") for y in glob(os.path.join(x[0], '*.png'))]
        expected_number_of_images = 140
        actual_number_of_images = len(all_image_files)

        # Assert
        self.assertEqual(expected_number_of_images, actual_number_of_images)

        # Cleanup
        os.remove(datasetDownloader.get_dataset_filename())
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
