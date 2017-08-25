import random
import sys
from typing import List

import numpy
from PIL import Image, ImageDraw
from sympy import Point2D

from omrdatasettools.image_generators.ExportPath import ExportPath
from omrdatasettools.image_generators.Rectangle import Rectangle


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
