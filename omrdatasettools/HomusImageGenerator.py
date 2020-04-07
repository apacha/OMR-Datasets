import argparse
import os
import random
import sys
from glob import glob
from typing import List

from PIL import Image, ImageDraw
from sympy import Point2D
from tqdm import tqdm

from omrdatasettools.ExportPath import ExportPath
from omrdatasettools.Rectangle import Rectangle


class HomusSymbol:
    def __init__(self, content: str, strokes: List[List[Point2D]], symbol_class: str, dimensions: Rectangle) -> None:
        super().__init__()
        self.dimensions = dimensions
        self.symbol_class = symbol_class
        self.content = content
        self.strokes = strokes

    @staticmethod
    def initialize_from_string(content: str) -> 'HomusSymbol':
        """
        Create and initializes a new symbol from a string

        :param content: The content of a symbol as read from the text-file
        :return: The initialized symbol
        :rtype: HomusSymbol
        """

        if content is None or content is "":
            return None

        lines = content.splitlines()
        min_x = sys.maxsize
        max_x = 0
        min_y = sys.maxsize
        max_y = 0

        symbol_name = lines[0]
        strokes = []

        for stroke_string in lines[1:]:
            stroke = []

            for point_string in stroke_string.split(";"):
                if point_string is "":
                    continue  # Skip the last element, that is due to a trailing ; in each line

                point_x, point_y = point_string.split(",")
                x = int(point_x)
                y = int(point_y)
                stroke.append(Point2D(x, y))

                max_x = max(max_x, x)
                min_x = min(min_x, x)
                max_y = max(max_y, y)
                min_y = min(min_y, y)

            strokes.append(stroke)

        dimensions = Rectangle(Point2D(min_x, min_y), max_x - min_x + 1, max_y - min_y + 1)
        return HomusSymbol(content, strokes, symbol_name, dimensions)

    def draw_into_bitmap(self, export_path: ExportPath, stroke_thickness: int, margin: int = 0) -> None:
        """
        Draws the symbol in the original size that it has plus an optional margin

        :param export_path: The path, where the symbols should be created on disk
        :param stroke_thickness: Pen-thickness for drawing the symbol in pixels
        :param margin: An optional margin for each symbol
        """
        self.draw_onto_canvas(export_path,
                              stroke_thickness,
                              margin,
                              self.dimensions.width + 2 * margin,
                              self.dimensions.height + 2 * margin)

    def draw_onto_canvas(self, export_path: ExportPath, stroke_thickness: int, margin: int, destination_width: int,
                         destination_height: int, staff_line_spacing: int = 14,
                         staff_line_vertical_offsets: List[int] = None,
                         bounding_boxes: dict = None, random_position_on_canvas: bool = False) -> None:
        """
        Draws the symbol onto a canvas with a fixed size

        :param bounding_boxes: The dictionary into which the bounding-boxes will be added of each generated image
        :param export_path: The path, where the symbols should be created on disk
        :param stroke_thickness:
        :param margin:
        :param destination_width:
        :param destination_height:
        :param staff_line_spacing:
        :param staff_line_vertical_offsets: Offsets used for drawing staff-lines. If None provided, no staff-lines will be drawn if multiple integers are provided, multiple images will be generated
        """
        width = self.dimensions.width + 2 * margin
        height = self.dimensions.height + 2 * margin
        if random_position_on_canvas:
            # max is required for elements that are larger than the canvas,
            # where the possible range for the random value would be negative
            random_horizontal_offset = random.randint(0, max(0, destination_width - width))
            random_vertical_offset = random.randint(0, max(0, destination_height - height))
            offset = Point2D(self.dimensions.origin.x - margin - random_horizontal_offset,
                             self.dimensions.origin.y - margin - random_vertical_offset)
        else:
            width_offset_for_centering = (destination_width - width) / 2
            height_offset_for_centering = (destination_height - height) / 2
            offset = Point2D(self.dimensions.origin.x - margin - width_offset_for_centering,
                             self.dimensions.origin.y - margin - height_offset_for_centering)

        image_without_staff_lines = Image.new('RGB', (destination_width, destination_height),
                                              "white")  # create a new white image
        draw = ImageDraw.Draw(image_without_staff_lines)
        black = (0, 0, 0)

        for stroke in self.strokes:
            for i in range(0, len(stroke) - 1):
                start_point = self.__subtract_offset(stroke[i], offset)
                end_point = self.__subtract_offset(stroke[i + 1], offset)
                draw.line((start_point.x, start_point.y, end_point.x, end_point.y), black, stroke_thickness)

        location = self.__subtract_offset(self.dimensions.origin, offset)
        bounding_box_in_image = Rectangle(location, self.dimensions.width, self.dimensions.height)
        # self.draw_bounding_box(draw, location)

        del draw

        if staff_line_vertical_offsets is not None and staff_line_vertical_offsets:
            for staff_line_vertical_offset in staff_line_vertical_offsets:
                image_with_staff_lines = image_without_staff_lines.copy()
                self.__draw_staff_lines_into_image(image_with_staff_lines, stroke_thickness,
                                                   staff_line_spacing, staff_line_vertical_offset)
                file_name_with_offset = export_path.get_full_path(staff_line_vertical_offset)
                image_with_staff_lines.save(file_name_with_offset)
                image_with_staff_lines.close()

                if bounding_boxes is not None:
                    # Note that the ImageDatasetGenerator does not yield the full path, but only the class_name and
                    # the file_name, e.g. '3-4-Time\\1-13_3_offset_74.png', so we store only that part in the dictionary
                    class_and_file_name = export_path.get_class_name_and_file_path(staff_line_vertical_offset)
                    bounding_boxes[class_and_file_name] = bounding_box_in_image
        else:
            image_without_staff_lines.save(export_path.get_full_path())
            if bounding_boxes is not None:
                # Note that the ImageDatasetGenerator does not yield the full path, but only the class_name and
                # the file_name, e.g. '3-4-Time\\1-13_3_offset_74.png', so we store only that part in the dictionary
                class_and_file_name = export_path.get_class_name_and_file_path()
                bounding_boxes[class_and_file_name] = bounding_box_in_image

        image_without_staff_lines.close()

    def draw_bounding_box(self, draw, location):
        red = (255, 0, 0)
        draw.rectangle(
            (location.x, location.y, location.x + self.dimensions.width, location.y + self.dimensions.height),
            fill=None, outline=red)

    @staticmethod
    def __draw_staff_lines_into_image(image: Image,
                                      stroke_thickness: int,
                                      staff_line_spacing: int = 14,
                                      vertical_offset=88):
        black = (0, 0, 0)
        width = image.width
        draw = ImageDraw.Draw(image)

        for i in range(5):
            y = vertical_offset + i * staff_line_spacing
            draw.line((0, y, width, y), black, stroke_thickness)
        del draw

    @staticmethod
    def __subtract_offset(a: Point2D, b: Point2D) -> Point2D:
        return Point2D(a.x - b.x, a.y - b.y)


class HomusImageGenerator:
    @staticmethod
    def create_images(raw_data_directory: str,
                      destination_directory: str,
                      stroke_thicknesses: List[int],
                      canvas_width: int = None,
                      canvas_height: int = None,
                      staff_line_spacing: int = 14,
                      staff_line_vertical_offsets: List[int] = None,
                      random_position_on_canvas: bool = False) -> dict:
        """
        Creates a visual representation of the Homus Dataset by parsing all text-files and the symbols as specified
        by the parameters by drawing lines that connect the points from each stroke of each symbol.

        Each symbol will be drawn in the center of a fixed canvas, specified by width and height.

        :param raw_data_directory: The directory, that contains the text-files that contain the textual representation
                                    of the music symbols
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        :param stroke_thicknesses: The thickness of the pen, used for drawing the lines in pixels. If multiple are
                                   specified, multiple images will be generated that have a different suffix, e.g.
                                   1-16-3.png for the 3-px version and 1-16-2.png for the 2-px version of the image 1-16
        :param canvas_width: The width of the canvas, that each image will be drawn upon, regardless of the original size of
                      the symbol. Larger symbols will be cropped. If the original size of the symbol should be used,
                      provided None here.
        :param canvas_height: The height of the canvas, that each image will be drawn upon, regardless of the original size of
                       the symbol. Larger symbols will be cropped. If the original size of the symbol should be used,
                       provided None here
        :param staff_line_spacing: Number of pixels spacing between each of the five staff-lines
        :param staff_line_vertical_offsets: List of vertical offsets, where the staff-lines will be superimposed over
                                            the drawn images. If None is provided, no staff-lines will be superimposed.
                                            If multiple values are provided, multiple versions of each symbol will be
                                            generated with the appropriate staff-lines, e.g. 1-5_3_offset_70.png and
                                            1-5_3_offset_77.png for two versions of the symbol 1-5 with stroke thickness
                                            3 and staff-line offsets 70 and 77 pixels from the top.
        :param random_position_on_canvas: True, if the symbols should be randomly placed on the fixed canvas.
                                          False, if the symbols should be centered in the fixed canvas.
                                          Note that this flag only has an effect, if fixed canvas sizes are used.
        :return: A dictionary that contains the file-names of all generated symbols and the respective bounding-boxes
                 of each symbol.
        """
        all_symbol_files = [y for x in os.walk(raw_data_directory) for y in glob(os.path.join(x[0], '*.txt'))]

        staff_line_multiplier = 1
        if staff_line_vertical_offsets is not None and staff_line_vertical_offsets:
            staff_line_multiplier = len(staff_line_vertical_offsets)

        total_number_of_symbols = len(all_symbol_files) * len(stroke_thicknesses) * staff_line_multiplier
        output = "Generating {0} images with {1} symbols in {2} different stroke thicknesses ({3})".format(
            total_number_of_symbols, len(all_symbol_files), len(stroke_thicknesses), stroke_thicknesses)

        if staff_line_vertical_offsets is not None:
            output += " and with staff-lines with {0} different offsets from the top ({1})".format(
                staff_line_multiplier, staff_line_vertical_offsets)

        if canvas_width is not None and canvas_height is not None:
            if random_position_on_canvas is False:
                output += "\nRandomly drawn on a fixed canvas of size {0}x{1} (Width x Height)".format(canvas_width,
                                                                                                       canvas_height)
            else:
                output += "\nCentrally drawn on a fixed canvas of size {0}x{1} (Width x Height)".format(canvas_width,
                                                                                                        canvas_height)

        print(output)
        print("In directory {0}".format(os.path.abspath(destination_directory)), flush=True)

        bounding_boxes = dict()

        progress_bar = tqdm(total=total_number_of_symbols, mininterval=0.25)
        for symbol_file in all_symbol_files:
            with open(symbol_file) as file:
                content = file.read()

            symbol = HomusSymbol.initialize_from_string(content)

            target_directory = os.path.join(destination_directory, symbol.symbol_class)
            os.makedirs(target_directory, exist_ok=True)

            raw_file_name_without_extension = os.path.splitext(os.path.basename(symbol_file))[0]

            for stroke_thickness in stroke_thicknesses:
                export_path = ExportPath(destination_directory, symbol.symbol_class, raw_file_name_without_extension,
                                         'png', stroke_thickness)
                if canvas_width is None and canvas_height is None:
                    symbol.draw_into_bitmap(export_path, stroke_thickness, margin=2)
                else:
                    symbol.draw_onto_canvas(export_path, stroke_thickness, 0, canvas_width,
                                            canvas_height, staff_line_spacing, staff_line_vertical_offsets,
                                            bounding_boxes, random_position_on_canvas)

                progress_bar.update(1 * staff_line_multiplier)

        progress_bar.close()
        return bounding_boxes

    @staticmethod
    def add_arguments_for_homus_image_generator(parser: argparse.ArgumentParser):
        parser.add_argument("-s", "--stroke_thicknesses", dest="stroke_thicknesses", default="3",
                            help="Stroke thicknesses for drawing the generated bitmaps. May define comma-separated list"
                                 " of multiple stroke thicknesses, e.g. '1,2,3'")
        parser.add_argument("--staff_line_spacing", default="14", type=int,
                            help="Spacing between two staff-lines in pixel")
        parser.add_argument("-offsets", "--staff_line_vertical_offsets", dest="offsets", default="",
                            help="Optional vertical offsets in pixel for drawing the symbols with superimposed "
                                 "staff-lines starting at this pixel-offset from the top. Multiple offsets possible, "
                                 "e.g. '81,88,95'")
        parser.add_argument("--disable_fixed_canvas_size", dest="use_fixed_canvas",
                            action="store_false",
                            help="True, if the images should be drawn on a fixed canvas with the specified width and height."
                                 "False to draw the symbols with their original sizes (each symbol might be different)")
        parser.set_defaults(use_fixed_canvas=True)
        parser.add_argument("--random_position_on_canvas", dest="random_position_on_canvas", action="store_true",
                            help="Provide this flag, if the symbols should be randomly placed on the fixed canvas."
                                 "Omit this flag, if the symbols should be centered in the fixed canvas (default)."
                                 "Note, that this flag only has an effect, if a fixed canvas size is used which gets "
                                 "disabled by the --disable_fixed_canvas_size flag.")
        parser.set_defaults(random_position_on_canvas=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/homus_raw",
        help="The directory, where the raw HOMUS dataset can be found (the text-files that contain the strokes)")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/images",
        help="The directory, where the generated bitmaps will be created")

    HomusImageGenerator.add_arguments_for_homus_image_generator(parser)
    parser.add_argument("--width", default="96", type=int, help="Width of the generated images in pixel")
    parser.add_argument("--height", default="96", type=int, help="Height of the generated images in pixel")

    flags, unparsed = parser.parse_known_args()

    offsets = []
    if flags.offsets != "":
        offsets = [int(o) for o in flags.offsets.split(',')]

    width, height = flags.width, flags.height
    if not flags.use_fixed_canvas:
        width, height = None, None

    HomusImageGenerator.create_images(flags.raw_dataset_directory,
                                      flags.image_dataset_directory,
                                      [int(s) for s in flags.stroke_thicknesses.split(',')],
                                      width,
                                      height,
                                      flags.staff_line_spacing,
                                      offsets,
                                      flags.random_position_on_canvas)
