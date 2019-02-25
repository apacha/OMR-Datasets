import json
import os

import argparse

from PIL import Image, ImageDraw, ImageColor
from tqdm import tqdm


class MeasureVisualizer:
    """
        Class that can be used to visualize the measure annotations that are provided as json files.
        Allows to enable/disable whether to draw system-measures (one measure for all instruments), stave-measures
        (one measure, single stave of one instrument) and staves (the whole line of a single instrument).
        System-measures contain all stave-measures that are being played simulatenously.

        Bounding boxes will be drawn with semitransparent colors.
    """
    def __init__(self, draw_system_measures: bool, draw_stave_measures: bool, draw_staves: bool) -> None:
        super().__init__()
        self.draw_system_measures = draw_system_measures
        self.draw_stave_measures = draw_stave_measures
        self.draw_staves = draw_staves

    def draw_bounding_boxes_for_all_images_in_directory(self, image_directory, json_annotation_directory):
        image_paths = os.listdir(image_directory)
        annotation_paths = os.listdir(json_annotation_directory)

        for image_path in tqdm(image_paths, desc="Drawing annotated images"):
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            annotations = [a for a in annotation_paths if image_name in a]
            # In case of a missing annotation, we skip that image by looping over the result, which would be an empty list
            for annotation_path in annotations:
                self.draw_bounding_boxes_into_image(os.path.join(image_directory, image_path),
                                                    os.path.join(json_annotation_directory, annotation_path))

    def draw_bounding_boxes_into_image(self, image_path: str, ground_truth_annotations_path: str):
        destination_path = image_path.replace(".png", "_annotated.png")
        image = Image.open(image_path)
        image = image.convert("RGB")

        with open(ground_truth_annotations_path, 'r') as gt_file:
            data = json.load(gt_file)

        blue = (0, 0, 255, 100)  # RGBA
        yellow = (255, 255, 0, 100)  # RGBA
        magenta = (255, 0, 255, 100)  # RGBA
        if self.draw_system_measures:
            self._draw_rectangles(data["system_measures"], image, blue)

        if self.draw_stave_measures:
            self._draw_rectangles(data["stave_measures"], image, magenta)

        if self.draw_staves:
            self._draw_rectangles(data["staves"], image, yellow)

        image.save(destination_path)

    def _draw_rectangles(self, rectangles, image, color):
        for rectangle in rectangles:
            left, top, bottom, right = rectangle["left"], rectangle["top"], rectangle["bottom"], \
                                       rectangle["right"]

            # String to float, float to int
            left = int(float(left))
            top = int(float(top))
            bottom = int(float(bottom))
            right = int(float(right))

            image_draw = ImageDraw.Draw(image, "RGBA")
            image_draw.rectangle([left, top, right, bottom], color)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Draw the bounding boxes from the ground-truth data.')
    parser.add_argument('--image_directory', dest='image_directory', type=str, help='Path to the images',
                        default="../data/muscima_pp/v1.0/data/images")
    parser.add_argument('--json_annotation_directory', dest='json_annotation_directory', type=str,
                        default="../data/muscima_pp/v1.0/data/json",
                        help='Path to the JSON annotations that contain the ground truth.')
    parser.add_argument('--system-measures', dest='system_measures', action='store_true')
    parser.add_argument('--no-system-measures', dest='system_measures', action='store_false')
    parser.set_defaults(system_measures=True)
    parser.add_argument('--stave-measures', dest='stave_measures', action='store_true')
    parser.add_argument('--no-stave-measures', dest='stave_measures', action='store_false')
    parser.set_defaults(stave_measures=True)
    parser.add_argument('--staves', dest='staves', action='store_true')
    parser.add_argument('--no-staves', dest='staves', action='store_false')
    parser.set_defaults(staves=True)
    args = parser.parse_args()

    visualizer = MeasureVisualizer(args.system_measures, args.stave_measures, args.staves)
    visualizer.draw_bounding_boxes_for_all_images_in_directory(args.image_directory, args.json_annotation_directory)
