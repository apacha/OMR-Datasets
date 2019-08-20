import os
import shutil
import unittest
from glob import glob

from omrdatasettools.downloaders.MuscimaPlusPlusDatasetDownloader import MuscimaPlusPlusDatasetDownloader
from omrdatasettools.image_generators.MuscimaPlusPlusMaskImageGenerator import \
    MuscimaPlusPlusMaskImageGenerator, MaskType


class MuscimaPlusPlusMaskImageGeneratorTest(unittest.TestCase):
    def test_render_node_masks_semantic_segmentation_of_nodes(self):
        # Arrange
        image_generator = MuscimaPlusPlusMaskImageGenerator()

        # Act
        image_generator.render_node_masks("testdata/muscima-pp_v2", "temp/muscima-pp_v2_masks", MaskType.NODES_SEMANTIC_SEGMENTATION)

        # Assert
        all_image_files = [y for x in os.walk("temp/muscima-pp_v2_masks") for y in glob(os.path.join(x[0], '*.png'))]
        expected_number_of_images = 1
        actual_number_of_images = len(all_image_files)
        self.assertEqual(expected_number_of_images, actual_number_of_images)

        # Cleanup
        shutil.rmtree("temp")

    def test_render_node_masks_instance_segmentation_of_staff_lines(self):
        # Arrange
        image_generator = MuscimaPlusPlusMaskImageGenerator()

        # Act
        image_generator.render_node_masks("testdata/muscima-pp_v2", "temp/muscima-pp_v2_masks", MaskType.STAFF_LINES_INSTANCE_SEGMENTATION)

        # Assert
        all_image_files = [y for x in os.walk("temp/muscima-pp_v2_masks") for y in glob(os.path.join(x[0], '*.png'))]
        expected_number_of_images = 1
        actual_number_of_images = len(all_image_files)
        self.assertEqual(expected_number_of_images, actual_number_of_images)

        # Cleanup
        shutil.rmtree("temp")

    def test_render_node_masks_instance_segmentation_of_staff_blobs(self):
        # Arrange
        image_generator = MuscimaPlusPlusMaskImageGenerator()

        # Act
        image_generator.render_node_masks("testdata/muscima-pp_v2", "temp/muscima-pp_v2_masks", MaskType.STAFF_BLOBS_INSTANCE_SEGMENTATION)

        # Assert
        all_image_files = [y for x in os.walk("temp/muscima-pp_v2_masks") for y in glob(os.path.join(x[0], '*.png'))]
        expected_number_of_images = 1
        actual_number_of_images = len(all_image_files)
        self.assertEqual(expected_number_of_images, actual_number_of_images)

        # Cleanup
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
