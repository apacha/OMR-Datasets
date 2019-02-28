import argparse
import os
from glob import glob

from PIL import Image, ImageOps
from tqdm import tqdm


class ImageColorInverter:
    """ Class for inverting white-on-black images to black-on-white images """

    def __init__(self) -> None:
        super().__init__()

    def invert_images(self, image_directory: str, image_file_ending: str = "*.bmp"):
        """
        In-situ converts the white on black images of a directory to black on white images

        :param image_directory: The directory, that contains the images
        :param image_file_ending: The pattern for finding files in the image_directory
        """
        image_paths = [y for x in os.walk(image_directory) for y in glob(os.path.join(x[0], image_file_ending))]
        for image_path in tqdm(image_paths, desc="Inverting all images in directory {0}".format(image_directory)):
            white_on_black_image = Image.open(image_path).convert("L")
            black_on_white_image = ImageOps.invert(white_on_black_image)
            black_on_white_image.save(os.path.splitext(image_path)[0] + ".png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image_directory",
        type=str,
        default="../data/fornes_raw",
        help="The directory, where a dataset can be found, that needs to be inverted, e.g. the original Fornés dataset")
    parser.add_argument("--image_file_ending", type=str, default="*.bmp", )

    flags, unparsed = parser.parse_known_args()

    image_inverter = ImageColorInverter()
    image_inverter.invert_images(flags.image_directory, flags.image_file_ending)
