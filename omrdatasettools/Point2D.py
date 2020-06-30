class Point2D():
    """A point in a 2-dimensional Euclidean space. """

    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Point2D) and self.x == o.x and self.y == o.y

