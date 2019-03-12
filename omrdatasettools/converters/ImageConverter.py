import argparse
from glob import glob

from PIL import Image
from tqdm import tqdm


class ImageConverter:
    def convert_grayscale_images_to_rgb_images(self, dataset_directory: str):
        image_files = glob(dataset_directory + "/**/*.png", recursive=True)

        for image_file in tqdm(image_files, desc="Converting images from 8-bit to 24-bit"):
            image = Image.open(image_file)  # type: Image.Image
            rgb_image = image.convert(mode="RGB")
            rgb_image.save(image_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converts images from 8-bit grayscale to 24-bit RGB images.')
    parser.add_argument("--dataset_directory", type=str, default="../data/muscima_pp",
                        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    image_converter = ImageConverter()
    image_converter.convert_grayscale_images_to_rgb_images(flags.dataset_directory)
