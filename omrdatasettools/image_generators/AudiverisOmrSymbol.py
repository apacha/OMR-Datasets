from sympy import Point2D

from omrdatasettools.image_generators.Rectangle import Rectangle


class AudiverisOmrSymbol(Rectangle):
    def __init__(self, symbol_class: str, x: int, y: int, width: int, height: int) -> None:
        super().__init__(Point2D(x, y), width, height)
        self.symbol_class = symbol_class
