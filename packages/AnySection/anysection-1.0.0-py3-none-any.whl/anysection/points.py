# anysection/geometry/points.py

class Point:
    """
    Class representing a point in 2D space.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        """
        Calculate the Euclidean distance to another point.
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def translate(self, dx, dy):
        """
        Translate the point by dx and dy.
        """
        self.x += dx
        self.y += dy

    def __str__(self):
        return f"Point({self.x}, {self.y})"
