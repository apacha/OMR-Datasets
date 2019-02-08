import os
import shutil
import unittest

from PIL import Image

from omrdatasettools.converters.ImageConverter import ImageConverter


class ImageConverterTest(unittest.TestCase):
    def test_download_extract_and_invert_bitmaps(self):
        # Arrange
        image = Image.new("L", (100, 100))
        os.makedirs("temp", exist_ok=True)
        image.save("temp/temp.png")
        image_converter = ImageConverter()

        # Act
        image_converter.convert_grayscale_images_to_rgb_images(".")

        # Assert
        converted_image = Image.open("temp/temp.png")  # type: Image.Image
        self.assertEqual("RGB", converted_image.mode)
        converted_image.close()

        # Cleanup
        shutil.rmtree("temp")


if __name__ == '__main__':
    unittest.main()
