from typing import Tuple

from sympy import Point2D


class Rectangle:
    def __init__(self, origin: Point2D, width: int, height: int):
        super().__init__()
        self.height = height
        self.width = width
        self.origin = origin  # Resembles the left top point
        self.left = origin.x
        self.top = origin.y
        self.right = self.left + self.width
        self.bottom = self.top + self.height

    @staticmethod
    def overlap(r1: 'Rectangle', r2: 'Rectangle'):
        """
        Overlapping rectangles overlap both horizontally & vertically
        """
        h_overlaps = (r1.left <= r2.right) and (r1.right >= r2.left)
        v_overlaps = (r1.bottom >= r2.top) and (r1.top <= r2.bottom)
        return h_overlaps and v_overlaps

    @staticmethod
    def merge(r1: 'Rectangle', r2: 'Rectangle') -> 'Rectangle':
        left = min(r1.left, r2.left)
        top = min(r1.top, r2.top)
        right = max(r1.right, r2.right)
        bottom = max(r1.bottom, r2.bottom)
        width = right - left
        height = bottom - top

        return Rectangle(Point2D(left, top), width, height)

    def as_bounding_box_with_margin(self, margin: int = 1) -> Tuple[int, int, int, int]:
        bounding_box_with_margin = (self.left - margin,
                                    self.top - margin,
                                    self.left + self.width + 2 * margin,
                                    self.top + self.height + 2 * margin)
        return bounding_box_with_margin

    def __eq__(self, o: object) -> bool:
        are_equal = self.width == o.width and self.height == o.height and self.origin == o.origin
        return are_equal

    def __str__(self) -> str:
        return "Rectangle[Origin:{0},{1}, Width:{2}, Height:{3}]".format(self.origin.x, self.origin.y, self.width,
                                                                         self.height)
