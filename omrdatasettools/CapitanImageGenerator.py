import argparse
import os
from typing import List

import numpy
from PIL import Image, ImageDraw
from sympy import Point2D
from tqdm import tqdm

from omrdatasettools.ExportPath import ExportPath
from omrdatasettools.Rectangle import Rectangle


class SimplePoint2D(object):
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class CapitanSymbol:
    def __init__(self, content: str, stroke: List[SimplePoint2D], image_data: numpy.ndarray, symbol_class: str,
                 dimensions: Rectangle) -> None:
        super().__init__()
        self.dimensions = dimensions
        self.symbol_class = symbol_class
        self.content = content
        self.stroke = stroke
        self.image_data = image_data

    @staticmethod
    def initialize_from_string(content: str) -> 'CapitanSymbol':
        """
        Create and initializes a new symbol from a string
        :param content: The content of a symbol as read from the text-file in the form <label>:<sequence>:<image>
        :return: The initialized symbol
        :rtype: CapitanSymbol
        """

        if content is None or content is "":
            return None

        parts = content.split(":")
        min_x = 100000
        max_x = 0
        min_y = 100000
        max_y = 0

        symbol_name = parts[0]

        sequence = parts[1]
        image_numbers = parts[2].split(',')
        image_data = numpy.asarray(image_numbers, numpy.uint8).reshape((30, 30))

        stroke = []

        for point_string in sequence.split(";"):
            if point_string is "":
                continue  # Skip the last element, that is due to a trailing ; in each line

            point_x, point_y = point_string.split(",")
            x = float(point_x)
            y = float(point_y)
            stroke.append(SimplePoint2D(x, y))

            max_x = max(max_x, x)
            min_x = min(min_x, x)
            max_y = max(max_y, y)
            min_y = min(min_y, y)

        dimensions = Rectangle(Point2D(min_x, min_y), int(max_x - min_x + 1), int(max_y - min_y + 1))
        return CapitanSymbol(content, stroke, image_data, symbol_name, dimensions)

    def draw_capitan_score_bitmap(self, export_path: ExportPath) -> None:
        """
        Draws the 30x30 symbol into the given file
        :param export_path: The path, where the symbols should be created on disk
        """
        with Image.fromarray(self.image_data, mode='L') as image:
            image.save(export_path.get_full_path())

    def draw_capitan_stroke_onto_canvas(self, export_path: ExportPath, stroke_thickness: int, margin: int):
        """
        Draws the symbol strokes onto a canvas
        :param export_path: The path, where the symbols should be created on disk
        :param stroke_thickness:
        :param margin:
        """
        width = int(self.dimensions.width + 2 * margin)
        height = int(self.dimensions.height + 2 * margin)
        offset = Point2D(self.dimensions.origin.x - margin, self.dimensions.origin.y - margin)

        image = Image.new('RGB', (width, height), "white")  # create a new white image
        draw = ImageDraw.Draw(image)
        black = (0, 0, 0)

        for i in range(0, len(self.stroke) - 1):
            start_point = self.__subtract_offset(self.stroke[i], offset)
            end_point = self.__subtract_offset(self.stroke[i + 1], offset)
            distance = self.__euclidean_distance(start_point, end_point)
            if distance > 1600:  # User moved more than 40 pixels - probably we should not draw a line here
                continue
            draw.line((start_point.x, start_point.y, end_point.x, end_point.y), black, stroke_thickness)

        del draw

        image.save(export_path.get_full_path())
        image.close()

    @staticmethod
    def __euclidean_distance(a: SimplePoint2D, b: SimplePoint2D) -> float:
        return (a.x - b.x) * (a.x - b.x) + abs(a.y - b.y) * abs(a.y - b.y)

    @staticmethod
    def __manhatten_distance(a: SimplePoint2D, b: SimplePoint2D) -> float:
        return abs(a.x - b.x) + abs(a.y - b.y)

    @staticmethod
    def __subtract_offset(a: SimplePoint2D, b: SimplePoint2D) -> SimplePoint2D:
        return SimplePoint2D(a.x - b.x, a.y - b.y)


class CapitanImageGenerator:
    def create_capitan_images(self, raw_data_directory: str,
                              destination_directory: str,
                              stroke_thicknesses: List[int]) -> None:
        """
        Creates a visual representation of the Capitan strokes by parsing all text-files and the symbols as specified
        by the parameters by drawing lines that connect the points from each stroke of each symbol.

        :param raw_data_directory: The directory, that contains the raw capitan dataset
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        :param stroke_thicknesses: The thickness of the pen, used for drawing the lines in pixels. If multiple are
                                   specified, multiple images will be generated that have a different suffix, e.g.
                                   1-16-3.png for the 3-px version and 1-16-2.png for the 2-px version of the image 1-16
        """
        symbols = self.load_capitan_symbols(raw_data_directory)
        self.draw_capitan_stroke_images(symbols, destination_directory, stroke_thicknesses)
        self.draw_capitan_score_images(symbols, destination_directory)

    def load_capitan_symbols(self, raw_data_directory: str) -> List[CapitanSymbol]:
        data_path = os.path.join(raw_data_directory, "BimodalHandwrittenSymbols", "data")
        with open(data_path) as file:
            data = file.read()

        symbol_strings = data.splitlines()
        symbols = []
        for symbol_string in tqdm(symbol_strings, desc="Loading symbols from strings"):
            symbol = CapitanSymbol.initialize_from_string(symbol_string)
            symbols.append(symbol)

        return symbols

    def draw_capitan_stroke_images(self, symbols: List[CapitanSymbol],
                                   destination_directory: str,
                                   stroke_thicknesses: List[int]) -> None:
        """
        Creates a visual representation of the Capitan strokes by drawing lines that connect the points
        from each stroke of each symbol.

        :param symbols: The list of parsed Capitan-symbols
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        :param stroke_thicknesses: The thickness of the pen, used for drawing the lines in pixels. If multiple are
                                   specified, multiple images will be generated that have a different suffix, e.g.
                                   1-16-3.png for the 3-px version and 1-16-2.png for the 2-px version of the image 1-16
        """

        total_number_of_symbols = len(symbols) * len(stroke_thicknesses)
        output = "Generating {0} images with {1} symbols in {2} different stroke thicknesses ({3})".format(
            total_number_of_symbols, len(symbols), len(stroke_thicknesses), stroke_thicknesses)

        print(output)
        print("In directory {0}".format(os.path.abspath(destination_directory)), flush=True)

        progress_bar = tqdm(total=total_number_of_symbols, mininterval=0.25, desc="Rendering strokes")
        capitan_file_name_counter = 0
        for symbol in symbols:
            capitan_file_name_counter += 1
            target_directory = os.path.join(destination_directory, symbol.symbol_class)
            os.makedirs(target_directory, exist_ok=True)

            raw_file_name_without_extension = "capitan-{0}-{1}-stroke".format(symbol.symbol_class,
                                                                              capitan_file_name_counter)

            for stroke_thickness in stroke_thicknesses:
                export_path = ExportPath(destination_directory, symbol.symbol_class, raw_file_name_without_extension,
                                         'png', stroke_thickness)
                symbol.draw_capitan_stroke_onto_canvas(export_path, stroke_thickness, 0)
                progress_bar.update(1)

        progress_bar.close()

    def draw_capitan_score_images(self, symbols: List[CapitanSymbol],
                                  destination_directory: str) -> None:
        """
        Draws the image data contained in each symbol

        :param symbols: The list of parsed Capitan-symbols
        :param destination_directory: The directory, in which the symbols should be generated into. One sub-folder per
                                      symbol category will be generated automatically
        :param stroke_thicknesses: The thickness of the pen, used for drawing the lines in pixels. If multiple are
                                   specified, multiple images will be generated that have a different suffix, e.g.
                                   1-16-3.png for the 3-px version and 1-16-2.png for the 2-px version of the image 1-16
        """

        total_number_of_symbols = len(symbols)
        output = "Generating {0} images from Capitan symbols".format(len(symbols))

        print(output)
        print("In directory {0}".format(os.path.abspath(destination_directory)), flush=True)

        progress_bar = tqdm(total=total_number_of_symbols, mininterval=0.25, desc="Rendering images")
        capitan_file_name_counter = 0
        for symbol in symbols:
            capitan_file_name_counter += 1
            target_directory = os.path.join(destination_directory, symbol.symbol_class)
            os.makedirs(target_directory, exist_ok=True)

            raw_file_name_without_extension = "capitan-{0}-{1}-score".format(symbol.symbol_class,
                                                                             capitan_file_name_counter)

            export_path = ExportPath(destination_directory, symbol.symbol_class, raw_file_name_without_extension, 'png')
            symbol.draw_capitan_score_bitmap(export_path)
            progress_bar.update(1)

        progress_bar.close()

    @staticmethod
    def add_arguments_for_homus_image_generator(parser: argparse.ArgumentParser):
        parser.add_argument("-s", "--stroke_thicknesses", dest="stroke_thicknesses", default="3",
                            help="Stroke thicknesses for drawing the generated bitmaps. May define comma-separated list"
                                 " of multiple stroke thicknesses, e.g. '1,2,3'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_dataset_directory",
        type=str,
        default="../data/capitan_raw",
        help="The directory, where the raw HOMUS dataset can be found (the text-files that contain the strokes)")
    parser.add_argument(
        "--image_dataset_directory",
        type=str,
        default="../data/images",
        help="The directory, where the generated bitmaps will be created")

    image_generator = CapitanImageGenerator()
    image_generator.add_arguments_for_homus_image_generator(parser)

    flags, unparsed = parser.parse_known_args()

    image_generator.create_capitan_images(flags.raw_dataset_directory, flags.image_dataset_directory,
                                          [int(s) for s in flags.stroke_thicknesses.split(',')])
