import argparse
import os
import shutil
from glob import glob


class ImageMover():

    def move_images(self, image_directory):
        """ Moves png-files one directory up from path/image/*.png -> path/*.png"""

        image_paths = glob(image_directory + "/**/*.png", recursive=True)
        for image_path in image_paths:
            destination = image_path.replace("\\image\\", "\\")
            shutil.move(image_path, destination)
        image_folders = glob(image_directory + "/**/image", recursive=True)
        for image_folder in image_folders:
            os.removedirs(image_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image_directory",
        type=str,
        default="../data",
        help="The directory, where a dataset can be found, that needs to be moved")

    flags, unparsed = parser.parse_known_args()

    image_mover = ImageMover()
    image_mover.move_images(flags.image_directory)
